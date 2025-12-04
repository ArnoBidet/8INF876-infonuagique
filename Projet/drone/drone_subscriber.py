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

print(f"Drone {DRONE_ID} - Broker MQTT configuré à l'adresse : {BROKER_ADDRESS}:{PORT}")

# Drone convoy parameters - moved in formation
FIELD_CENTER = (46.9131, -71.2085)  # 10km north of Quebec City
convoy_drones = []
start_time = None  # Track start time for relative movement

def generate_convoy_drones(t=None):
    """Generate drone convoy positions moving in formation"""
    global start_time
    
    if start_time is None:
        start_time = time.time()
    
    # Calculate elapsed time in seconds since start
    elapsed_time = time.time() - start_time
    
    cx, cy = FIELD_CENTER
    
    # Move convoy very slowly westward (much slower than cows)
    westward_speed = 0.00005  # degrees per second (très lent)
    west_offset = -westward_speed * elapsed_time
    
    # Square formation parameters
    formation_size = 0.004  # Size of square formation in degrees
    
    drones = []
    num_drones = 4  # Convoy of 4 drones
    
    # Square formation positions (corners of a square)
    square_positions = [
        (-formation_size/2, -formation_size/2),  # Bottom-left
        (formation_size/2, -formation_size/2),   # Bottom-right  
        (formation_size/2, formation_size/2),    # Top-right
        (-formation_size/2, formation_size/2)    # Top-left
    ]
    
    for i in range(num_drones):
        # Get square formation offset
        lat_offset, lng_offset = square_positions[i]
        
        lat = cx + lat_offset
        lng = cy + west_offset + lng_offset
        
        drones.append({
            'id': f'drone_{DRONE_ID}_{i}',  # Include drone ID for uniqueness
            'lat': lat,
            'lng': lng,
            'radius': 800 + i * 200  # Coverage radius in meters
        })
    
    return drones

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
            
            # Generate current drone positions
            current_drones = generate_convoy_drones()
            
            # Compute surveillance zone (convex hull of drones)
            if len(current_drones) >= 3:
                zone_polygon = compute_convex_hull(current_drones)
                
                # Calculate zone center
                if zone_polygon:
                    zone_center_lat = sum(p['lat'] for p in zone_polygon) / len(zone_polygon)
                    zone_center_lng = sum(p['lng'] for p in zone_polygon) / len(zone_polygon)
                    
                    # Publish zone update for cows
                    zone_update = {
                        'center': {'lat': zone_center_lat, 'lng': zone_center_lng},
                        'polygon': zone_polygon,
                        'drones': current_drones,
                        'timestamp': time.time()
                    }
                    
                    client.publish(TOPIC_ZONE_UPDATE, json.dumps(zone_update), qos=1)
                    
                    # Count cows outside zone
                    outside_cows = [cow for cow in cows_data if cow.get('outside_zone', False)]
                    
                    print(f"[{time.strftime('%H:%M:%S')}] Drone {DRONE_ID}: Zone mise à jour, "
                          f"{len(cows_data)} vaches détectées, {len(outside_cows)} hors zone")
        
    except Exception as e:
        print(f"Erreur lors du traitement du message : {e}")



def publish_drone_positions_periodically():
    """Publish drone positions and zone information periodically"""
    while True:
        try:
            # Only drone 1 publishes the zone information to avoid conflicts
            if DRONE_ID == "1":
                # Generate current drone positions
                current_drones = generate_convoy_drones()
                
                # Compute surveillance zone (convex hull of drones)
                if len(current_drones) >= 3:
                    zone_polygon = compute_convex_hull(current_drones)
                    
                    # Calculate zone center
                    if zone_polygon:
                        zone_center_lat = sum(p['lat'] for p in zone_polygon) / len(zone_polygon)
                        zone_center_lng = sum(p['lng'] for p in zone_polygon) / len(zone_polygon)
                        
                        # Publish zone update
                        zone_update = {
                            'center': {'lat': zone_center_lat, 'lng': zone_center_lng},
                            'polygon': zone_polygon,
                            'drones': current_drones,
                            'timestamp': time.time(),
                            'drone_id': DRONE_ID
                        }
                        
                        client.publish(TOPIC_ZONE_UPDATE, json.dumps(zone_update), qos=1)
                        
                        print(f"[{time.strftime('%H:%M:%S')}] Drone {DRONE_ID}: Zone publiée avec {len(current_drones)} drones, zone: {len(zone_polygon)} points")
                else:
                    print(f"[{time.strftime('%H:%M:%S')}] Drone {DRONE_ID}: Pas assez de drones pour former une zone")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Drone {DRONE_ID}: En attente (seul drone1 publie la zone)")
            
            time.sleep(3)  # Publish every 3 seconds
            
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