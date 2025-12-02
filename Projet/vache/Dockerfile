# Utilisation d'une image Python stable et légère
FROM python:3.10-slim

# Définition du répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copie et installation des dépendances (paho-mqtt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du script d'exécution de la vache
COPY vache_publisher.py .

# Commande de lancement de l'application
# Elle exécute le script Python simple
CMD ["python", "vache_publisher.py"]