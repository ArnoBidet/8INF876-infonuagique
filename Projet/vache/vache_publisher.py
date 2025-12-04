import paho.mqtt.client as mqtt
import time
import os
import json
from cow_movement import CowHerd, Vector2D

# Configuration
BROKER_ADDRESS = os.environ.get("MQTT_BROKER", "mqtt-broker")
PORT = 1883
TOPIC_POSITIONS = "vaches/positions"
TOPIC_ZONE_UPDATE = "drones/zone"

# Field location (10km north of Quebec City)
FIELD_CENTER = (46.9131, -71.2085)  # 10km north of Quebec City

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cow_herd = CowHerd(FIELD_CENTER, num_cows=25)

def on_message(client, userdata, msg):
    """Handle incoming messages about drone zone updates"""
    try:
        if msg.topic == TOPIC_ZONE_UPDATE:
            zone_data = json.loads(msg.payload.decode())
            print(f"[VACHES] Zone update received: {zone_data.keys()}")
            
            if 'center' in zone_data and 'polygon' in zone_data:
                # Store drone center for herd movement
                drone_center = Vector2D(zone_data['center']['lat'], zone_data['center']['lng'])
                cow_herd.last_drone_center = drone_center
                
                # Update zone exit detection
                polygon = [(point['lat'], point['lng']) for point in zone_data['polygon']]
                cow_herd.check_zone_exits(polygon)
                print(f"[VACHES] Zone update: {len(polygon)} polygon points, center: [{zone_data['center']['lat']:.6f}, {zone_data['center']['lng']:.6f}]")
            else:
                print(f"[VACHES] Invalid zone data received: {zone_data}")
    except Exception as e:
        print(f"[VACHES] Error processing zone update: {e}")

def run_publisher():
    try:
        # 🚨 IMPORTANT : Attendre 5 secondes pour garantir que le Broker est opérationnel
        print("Temporisation de 5 secondes pour s'assurer que le Broker est prêt...")
        time.sleep(5) 
        
        client.on_message = on_message
        client.connect(BROKER_ADDRESS, PORT, 60)
        client.subscribe(TOPIC_ZONE_UPDATE)
        client.loop_start() # Démarrer le thread de boucle réseau pour les publications

        print(f"Publisher VACHES connecté à {BROKER_ADDRESS}")
        print(f"Troupeau initialisé avec {len(cow_herd.cows)} vaches au centre {FIELD_CENTER}")

        while True:
            # Update cow movement with flocking behavior - pass drone zone if available
            drone_zone_center = None
            if hasattr(cow_herd, 'last_drone_center'):
                drone_zone_center = cow_herd.last_drone_center
            
            cow_herd.update(drone_zone_center)
            
            # Publish cow positions
            cows_data = cow_herd.get_cows_data()
            payload = json.dumps({
                'timestamp': time.time(),
                'cows': cows_data,
                'field_center': {'lat': FIELD_CENTER[0], 'lng': FIELD_CENTER[1]}
            })
            
            client.publish(TOPIC_POSITIONS, payload, qos=1)
            
            # Log summary
            outside_count = sum(1 for cow in cow_herd.cows if cow.outside_zone)
            total_cows = len(cows_data)
            print(f"[VACHES {time.strftime('%H:%M:%S')}] Publié {total_cows} vaches: {total_cows-outside_count} dans zone, {outside_count} hors zone")
            
            time.sleep(2) # Update every 2 seconds
            
    except Exception as e:
        print(f"Erreur fatale : {e}")
        time.sleep(10)

if __name__ == '__main__':
    run_publisher()