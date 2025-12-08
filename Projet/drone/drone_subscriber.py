import paho.mqtt.client as mqtt
import time
import os
import json
import math
import random

time.sleep(3) # Ajout d'une attente pour s'assurer que le broker MQTT est prêt

BROKER_ADDRESS = os.environ.get("MQTT_BROKER", "mqtt-broker")
PORT = 1883
DRONE_ID = os.environ.get("DRONE_ID", "1")
TOPIC_COW_POSITIONS = "vaches/positions"
TOPIC_ZONE_UPDATE = "drones/zone"
TOPIC_DRONE_POSITIONS = "drones/positions"

# Drone individual parameters from environment variables
DRONE_START_LAT = float(os.environ.get("DRONE_START_LAT", "46.9131"))
DRONE_START_LNG = float(os.environ.get("DRONE_START_LNG", "-71.2085"))
DRONE_RADIUS = int(os.environ.get("DRONE_RADIUS", "800"))

print(f"Drone {DRONE_ID} - Broker MQTT configuré à l'adresse : {BROKER_ADDRESS}:{PORT}")
print(f"Drone {DRONE_ID} - Position de départ: ({DRONE_START_LAT}, {DRONE_START_LNG}), Rayon: {DRONE_RADIUS}m")

start_time = None  # Track start time for relative movement

# Décentralized coordination - each drone maintains other drones' positions
other_drones = {}  # {drone_id: {'data': drone_data, 'timestamp': timestamp}}
import threading
drone_lock = threading.Lock()

def generate_single_drone():
    """Generate single drone position with movement pattern"""
    global start_time
    
    if start_time is None:
        start_time = time.time()
    
    # Calculate elapsed time in seconds since start
    elapsed_time = time.time() - start_time
    
    # Move drone slowly westward
    westward_speed = 0.00005  # degrees per second (très lent)
    west_offset = -westward_speed * elapsed_time
    
    # Simple circular patrol pattern around starting position
    patrol_radius = 0.002  # Small patrol radius in degrees
    patrol_speed = 0.1  # radians per second
    angle = patrol_speed * elapsed_time
    
    lat_offset = patrol_radius * math.cos(angle)
    lng_offset = patrol_radius * math.sin(angle)
    
    lat = DRONE_START_LAT + lat_offset
    lng = DRONE_START_LNG + west_offset + lng_offset
    
    return {
        'id': f'drone_{DRONE_ID}',
        'lat': lat,
        'lng': lng,
        'radius': DRONE_RADIUS
    }

def compute_convex_hull(points):
    """Compute convex hull using monotonic chain algorithm"""
    if len(points) <= 1:
        return points
    
    def cross(o, a, b):
        return (a[0]-o[0]) * (b[1]-o[1]) - (a[1]-o[1]) * (b[0]-o[0])
    
    pts = sorted([(p['lat'], p['lng']) for p in points])
    
    # Build lower hull
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    
    # Build upper hull
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    
    hull = lower[:-1] + upper[:-1]
    return [{'lat': p[0], 'lng': p[1]} for p in hull]

def is_leader():
    """Determine if this drone should act as leader for zone calculation"""
    # Simple leadership: drone with lowest ID that has seen other drones
    with drone_lock:
        all_drone_ids = [DRONE_ID] + list(other_drones.keys())
        return DRONE_ID == min(all_drone_ids)

# ----------------- Fonctions de Callback MQTT -----------------

def on_connect(client, userdata, flags, rc, properties):
    """Callback appelé lorsque le client se connecte au broker."""
    if rc == 0:
        print(f"Drone {DRONE_ID} connecté au Broker !")
        client.subscribe(TOPIC_COW_POSITIONS)
        client.subscribe(TOPIC_DRONE_POSITIONS)
        print(f"Abonné aux topics: {TOPIC_COW_POSITIONS}, {TOPIC_DRONE_POSITIONS}")
    else:
        print(f"Échec de la connexion, code retour : {rc}")

def on_message(client, userdata, msg):
    """Callback appelé lorsqu'un message est reçu sur un topic abonné."""
    try:
        if msg.topic == TOPIC_COW_POSITIONS:
            payload = json.loads(msg.payload.decode("utf-8"))
            cows_data = payload.get('cows', [])
            
            # Only leader calculates and publishes zone when cows are detected
            if is_leader():
                calculate_and_publish_zone(client, cows_data)
        
        elif msg.topic == TOPIC_DRONE_POSITIONS:
            # Store other drones' positions for decentralized coordination
            payload = json.loads(msg.payload.decode("utf-8"))
            other_drone_id = payload.get('drone_id')
            drone_data = payload.get('drone', {})
            timestamp = payload.get('timestamp', time.time())
            
            if other_drone_id != DRONE_ID and drone_data:
                with drone_lock:
                    other_drones[other_drone_id] = {
                        'data': drone_data,
                        'timestamp': timestamp
                    }
                
                print(f"[{time.strftime('%H:%M:%S')}] Drone {DRONE_ID}: Position reçue du drone {other_drone_id} "
                      f"lat={drone_data.get('lat', 0):.6f}, lng={drone_data.get('lng', 0):.6f}")
        
    except Exception as e:
        print(f"Erreur lors du traitement du message : {e}")

def calculate_and_publish_zone(client, cows_data):
    """Calculate surveillance zone based on all known drone positions"""
    try:
        # Get current drone position
        current_drone = generate_single_drone()
        
        # Collect all active drone positions
        all_drones = [current_drone]
        
        with drone_lock:
            # Clean up old drone positions (older than 15 seconds)
            current_time = time.time()
            active_drones = {
                drone_id: info for drone_id, info in other_drones.items()
                if current_time - info['timestamp'] < 15
            }
            other_drones.clear()
            other_drones.update(active_drones)
            
            # Add active other drones
            for info in active_drones.values():
                all_drones.append(info['data'])
        
        # Calculate zone if we have enough drones
        if len(all_drones) >= 3:
            zone_polygon = compute_convex_hull(all_drones)
            
            # Calculate zone center
            if zone_polygon:
                zone_center_lat = sum(p['lat'] for p in zone_polygon) / len(zone_polygon)
                zone_center_lng = sum(p['lng'] for p in zone_polygon) / len(zone_polygon)
                
                # Publish zone update
                zone_update = {
                    'center': {'lat': zone_center_lat, 'lng': zone_center_lng},
                    'polygon': zone_polygon,
                    'drones': all_drones,
                    'timestamp': time.time(),
                    'leader_drone_id': DRONE_ID,
                    'total_drones': len(all_drones)
                }
                
                client.publish(TOPIC_ZONE_UPDATE, json.dumps(zone_update), qos=1)
                
                # Count cows outside zone (simple approximation)
                outside_cows = [cow for cow in cows_data if cow.get('outside_zone', False)]
                
                print(f"[{time.strftime('%H:%M:%S')}] Drone {DRONE_ID} (LEADER): Zone publiée avec {len(all_drones)} drones, "
                      f"{len(cows_data)} vaches détectées, {len(outside_cows)} hors zone")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Drone {DRONE_ID}: Pas assez de drones pour former une zone ({len(all_drones)})")
            
    except Exception as e:
        print(f"Erreur lors du calcul de zone : {e}")



def publish_drone_positions_periodically():
    """Publish individual drone position periodically"""
    while True:
        try:
            # Generate current drone position
            current_drone = generate_single_drone()
            
            # Publish individual drone position
            drone_position = {
                'drone': current_drone,
                'timestamp': time.time(),
                'drone_id': DRONE_ID
            }
            
            client.publish(TOPIC_DRONE_POSITIONS, json.dumps(drone_position), qos=1)
            
            # Show leadership status
            leader_status = " (LEADER)" if is_leader() else ""
            active_count = len(other_drones) + 1  # +1 for self
            
            print(f"[{time.strftime('%H:%M:%S')}] Drone {DRONE_ID}{leader_status}: Position publiée "
                  f"lat={current_drone['lat']:.6f}, lng={current_drone['lng']:.6f}, "
                  f"rayon={current_drone['radius']}m, drones actifs: {active_count}")
            
            time.sleep(3)  # Publish every 3 seconds for better coordination
            
        except Exception as e:
            print(f"Erreur lors de la publication : {e}")
            time.sleep(5)

# ----------------- Logique d'exécution -----------------

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message

print(f"Tentative de connexion au Broker MQTT à {BROKER_ADDRESS}:{PORT}...")

try:
    client.connect(BROKER_ADDRESS, PORT, 60)
    
    # Start the periodic drone position publishing in a separate thread
    import threading
    drone_thread = threading.Thread(target=publish_drone_positions_periodically, daemon=True)
    drone_thread.start()
    
    # Lancement de la boucle de réseau en mode bloquant, le subscriber écoute en permanence
    client.loop_forever() 

except Exception as e:
    print(f"Connexion MQTT échouée : {e}")
    time.sleep(5)