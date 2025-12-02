import paho.mqtt.client as mqtt
import time
import os

time.sleep(3) # Ajout d'une attente pour s'assurer que le broker MQTT est prêt

BROKER_ADDRESS = os.environ.get("MQTT_BROKER", "mqtt-broker")
PORT = 1883
TOPIC_TO_SUBSCRIBE = "vaches/etat_sante" # Le drone écoute les vaches
print(f"Broker MQTT configuré à l'adresse : {BROKER_ADDRESS}:{PORT}")

# ----------------- Fonctions de Callback MQTT -----------------

def on_connect(client, userdata, flags, rc, properties):
    """Callback appelé lorsque le client se connecte au broker."""
    if rc == 0:
        print("Subscriber DRONE connecté au Broker !")
        # S'abonner dès la connexion réussie
        client.subscribe(TOPIC_TO_SUBSCRIBE)
        print(f"Abonné au topic: {TOPIC_TO_SUBSCRIBE}")
    else:
        print(f"Échec de la connexion, code retour : {rc}")

def on_message(client, userdata, msg):
    """Callback appelé lorsqu'un message est reçu sur un topic abonné."""
    try:
        # Décoder le payload du message
        print(2)
        payload = msg.payload.decode("utf-8")
        
        print(f"\n<<< NOUVELLE ALERTE VACHE >>>")
        print(f"Topic: {msg.topic}")
        print(f"Message: {payload}")
        
        # Logique métier: Analyser le message
        if "Pouls:70" in payload:
            print("--- ACTION DU DRONE : Pouls élevé détecté. Démarrage du survol de zone. ---")
        
    except Exception as e:
        print(f"Erreur lors du traitement du message : {e}")



# ----------------- Logique d'exécution -----------------

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message

print(f"Tentative de connexion au Broker MQTT à {BROKER_ADDRESS}:{PORT}...")

try:
    client.connect(BROKER_ADDRESS, PORT, 60)
    # Lancement de la boucle de réseau en mode bloquant, le subscriber écoute en permanence
    client.loop_forever() 

except Exception as e:
    print(f"Connexion MQTT échouée : {e}")
    time.sleep(5)