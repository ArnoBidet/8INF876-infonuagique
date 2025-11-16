import os
import time
import threading
import math
import random
from collections import deque
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests

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

# Simulated entities (if no external source). Each entity: {'id', 'lat', 'lng'}
entities = []

# Center for simulation / map (default around Quebec City)
MAP_CENTER = (46.8139, -71.2080)


def init_entities():
    global entities
    entities = []
    base_lat, base_lng = MAP_CENTER
    for i in range(ENTITIES_COUNT):
        # scatter within ~0.05 degrees
        lat = base_lat + random.uniform(-0.05, 0.05)
        lng = base_lng + random.uniform(-0.05, 0.05)
        entities.append({'id': i, 'lat': lat, 'lng': lng})


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


# Initialize entities at import time (works with gunicorn workers)
init_entities()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/state')
def api_state():
    # Move simulated entities a bit
    move_entities()

    # Get drones from URLs or simulate
    drones = fetch_drones_from_urls()
    if not drones:
        drones = simulated_drones()

    # compute convex hull of drone lat/lng as polygon
    pts = [(d['lat'], d['lng']) for d in drones]
    hull = monotonic_chain_convex_hull(pts)

    # count entities inside hull
    in_count = 0
    out_count = 0
    for e in entities:
        if point_in_polygon(e['lat'], e['lng'], hull):
            in_count += 1
        else:
            out_count += 1

    # append to history
    now = int(time.time())
    history.append({'ts': now, 'in': in_count, 'out': out_count})

    # prepare time series arrays (last N)
    times = [h['ts'] for h in history]
    ins = [h['in'] for h in history]
    outs = [h['out'] for h in history]

    return jsonify({
        'timestamp': now,
        'drones': drones,
        'hull': [{'lat': p[0], 'lng': p[1]} for p in hull],
        'entities_count': len(entities),
        'counts': {'in': in_count, 'out': out_count},
        'timeseries': {'t': times, 'in': ins, 'out': outs},
        'center': {'lat': MAP_CENTER[0], 'lng': MAP_CENTER[1]}
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
