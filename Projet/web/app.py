import os
import time
import threading
import math
import random
import json
from collections import deque
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
import paho.mqtt.client as mqtt

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Configuration
DRONE_URLS = os.getenv('DRONE_URLS')
if DRONE_URLS:
    DRONE_URLS = [u.strip() for u in DRONE_URLS.split(',') if u.strip()]

ENTITIES_COUNT = int(os.getenv('ENTITIES_COUNT', '100'))
HISTORY_MAX = int(os.getenv('HISTORY_MAX', '300'))

# In-memory time series of counts (timestamp, in_count, out_count)
history = deque(maxlen=HISTORY_MAX)

# Real-time data from MQTT
current_cows = []
current_drones = []
current_zone = []

# Center for simulation / map (10km north of Quebec City)
MAP_CENTER = (46.9131, -71.2085)

# MQTT Configuration
MQTT_BROKER = os.getenv('MQTT_BROKER', 'mqtt-broker')
MQTT_PORT = 1883


# MQTT callback functions
def on_mqtt_connect(client, userdata, flags, rc, properties):
    """Called when MQTT client connects"""
    if rc == 0:
        print("Web app connected to MQTT broker")
        client.subscribe("vaches/positions")
        client.subscribe("drones/zone")
    else:
        print(f"Failed to connect to MQTT broker: {rc}")

def on_mqtt_message(client, userdata, msg):
    """Called when MQTT message is received"""
    global current_cows, current_drones, current_zone, history
    
    try:
        payload = json.loads(msg.payload.decode())
        print(f"[WEB] MQTT message received on {msg.topic}: {len(str(payload))} chars")
        
        if msg.topic == "vaches/positions":
            current_cows = payload.get('cows', [])
            print(f"[WEB] Updated {len(current_cows)} cows")
            
        elif msg.topic == "drones/zone":
            current_drones = payload.get('drones', [])
            current_zone = payload.get('polygon', [])
            print(f"[WEB] Updated {len(current_drones)} drones, zone with {len(current_zone)} points")
            
            # Update history with in/out counts
            if current_cows:
                in_count = len([cow for cow in current_cows if not cow.get('outside_zone', False)])
                out_count = len([cow for cow in current_cows if cow.get('outside_zone', False)])
                
                now = int(time.time())
                history.append({'ts': now, 'in': in_count, 'out': out_count})
                
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

# Initialize MQTT client
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_mqtt_connect  
mqtt_client.on_message = on_mqtt_message

def init_mqtt():
    """Initialize MQTT connection"""
    try:
        print(f"[WEB] Attempting to connect to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        print(f"[WEB] MQTT client started")
    except Exception as e:
        print(f"[WEB] Failed to connect to MQTT: {e}")
        print(f"[WEB] Will continue without MQTT - using fallback data")


def move_entities():
    for e in entities:
        e['lat'] += random.uniform(-0.0008, 0.0008)
        e['lng'] += random.uniform(-0.0008, 0.0008)


def fetch_drones_from_urls():
    drones = []
    if not DRONE_URLS:
        return drones
    for url in DRONE_URLS:
        try:
            r = requests.get(url, timeout=1.0)
            r.raise_for_status()
            data = r.json()
            if isinstance(data, dict):
                # maybe single drone
                data = [data]
            for d in data:
                # expect id, lat, lng, radius
                if all(k in d for k in ('lat', 'lng')):
                    drones.append({'id': d.get('id', url), 'lat': float(d['lat']), 'lng': float(d['lng']), 'radius': float(d.get('radius', 100))})
        except Exception:
            continue
    return drones


def simulated_drones(t=None):
    # produce 3 simulated drones moving in circular patterns
    if t is None:
        t = time.time()
    cx, cy = MAP_CENTER
    drones = []
    for i in range(3):
        ang = t * 0.2 + i * 2.0
        lat = cx + 0.01 * math.cos(ang) + i * 0.003
        lng = cy + 0.01 * math.sin(ang) + i * 0.003
        drones.append({'id': f'sim{i}', 'lat': lat, 'lng': lng, 'radius': 1000 + i * 200})
    return drones


def monotonic_chain_convex_hull(points):
    # points: list of (x,y)
    pts = sorted(points)
    if len(pts) <= 1:
        return pts

    def cross(o, a, b):
        return (a[0]-o[0]) * (b[1]-o[1]) - (a[1]-o[1]) * (b[0]-o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    hull = lower[:-1] + upper[:-1]
    return hull


def point_in_polygon(x, y, poly):
    # ray casting algorithm
    inside = False
    n = len(poly)
    if n == 0:
        return False
    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        if min(p1y, p2y) < y <= max(p1y, p2y) and x <= max(p1x, p2x):
            if p1y != p2y:
                xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
            if p1x == p2x or x <= xinters:
                inside = not inside
        p1x, p1y = p2x, p2y
    return inside


# Initialize MQTT connection at import time
init_mqtt()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/state')
def api_state():
    global current_cows, current_drones, current_zone
    
    now = int(time.time())
    
    # Count cows in/out of zone
    if current_cows:
        in_count = len([cow for cow in current_cows if not cow.get('outside_zone', False)])
        out_count = len([cow for cow in current_cows if cow.get('outside_zone', False)])
    else:
        in_count, out_count = 0, 0
    
    # Prepare time series arrays (last N)
    times = [h['ts'] for h in history]
    ins = [h['in'] for h in history]
    outs = [h['out'] for h in history]
    
    # Add current data to history if not recent
    if not history or (now - history[-1]['ts']) > 5:
        history.append({'ts': now, 'in': in_count, 'out': out_count})

    print(f"[API] Returning: {len(current_drones)} drones, {len(current_cows)} cows, {len(current_zone)} zone points")

    return jsonify({
        'timestamp': now,
        'drones': current_drones,
        'cows': current_cows,
        'hull': current_zone,
        'entities_count': len(current_cows),
        'counts': {'in': in_count, 'out': out_count},
        'timeseries': {'t': times, 'in': ins, 'out': outs},
        'center': {'lat': MAP_CENTER[0], 'lng': MAP_CENTER[1]}
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
