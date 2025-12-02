import paho.mqtt.client as mqtt
import time
import os
import random

# Configuration
BROKER_ADDRESS = os.environ.get("MQTT_BROKER", "mqtt-broker")
PORT = 1883
TOPIC_SANTE = "vaches/etat_sante"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def run_publisher():
    try:
        # 🚨 IMPORTANT : Attendre 5 secondes pour garantir que le Broker est opérationnel
        print("Temporisation de 5 secondes pour s'assurer que le Broker est prêt...")
        time.sleep(5) 
        
        client.connect(BROKER_ADDRESS, PORT, 60)
        client.loop_start() # Démarrer le thread de boucle réseau pour les publications

        print(f"Publisher VACHES connecté à {BROKER_ADDRESS}")
        
        id_vache = 42

        while True:
            # Simulation de données
            pouls = random.randint(55, 75)
            
            # Publie le message
            payload = f"Vache ID:{id_vache}, Pouls:{pouls} bpm"
            client.publish(TOPIC_SANTE, payload, qos=1) # QoS 1 garantit la livraison
            print(f"[{time.strftime('%H:%M:%S')}] Publié sur {TOPIC_SANTE}: {payload}")
            
            time.sleep(3) # Envoi régulier
            
    except Exception as e:
        print(f"Erreur fatale : {e}")
        time.sleep(10)

if __name__ == '__main__':
    run_publisher()