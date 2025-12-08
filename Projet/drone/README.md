# Module Drone - Surveillance de Vaches par Drones

Ce module fournit un système de surveillance de vaches utilisant des drones individuels qui communiquent via MQTT.

## 🏗️ Architecture

Le module est maintenant organisé avec des services individuels pour chaque drone :

```
drone/
├── __init__.py              # Interface publique du package
├── drone.py                 # Module principal (rétrocompatibilité)
├── geometry.py              # Calculs géométriques
├── cow_detection.py         # Détection et alertes
├── drone_service.py         # Service principal orchestrateur
├── drone_subscriber.py      # Service individuel par drone
└── zone_coordinator.py      # Service de coordination des zones
```

## 🚀 Système de Drones Complètement Décentralisé

### Architecture Décentralisée

**Drones autonomes** (`drone_subscriber.py`) :
- Chaque service drone ne gère qu'un seul drone
- Position de départ et rayon configurables via variables d'environnement
- Publie sa position individuelle sur le topic MQTT `drones/positions`
- Écoute les positions des autres drones pour coordination
- Calcule lui-même la zone de surveillance globale (pas de service centralisé)
- Système de leadership automatique pour éviter les conflits
- Patrouille selon un motif circulaire autour de sa position de départ

### 📁 Description des modules

#### `geometry.py` - Calculs géométriques
- **`cross_product(o, a, b)`** : Calcule le produit vectoriel pour déterminer l'orientation
- **`convex_hull(entities)`** : Calcule l'enveloppe convexe d'un ensemble de points

#### `cow_detection.py` - Détection et alertes  
- **`detect_cow_in_hull(hull)`** : Détecte la présence de vaches dans l'enveloppe
- **`print_alert(cows)`** : Affiche les informations d'alerte
- **`alert(hull)`** : Orchestrateur principal pour la détection et l'alerte

#### `drone_service.py` - Service principal
- **`DroneService`** : Classe principale avec méthodes statiques
  - `analyze_perimeter(entities)` : Analyse complète du périmètre
  - `monitor_and_alert(entities)` : Surveillance et alerte automatique

#### `drone.py` - Rétrocompatibilité
- Module maintenu pour la compatibilité avec l'ancien code
- **DEPRECATED** : Utilisez les modules spécialisés pour les nouveaux développements

## 🚀 Utilisation

### Utilisation moderne (recommandée)

```python
from drone import DroneService, convex_hull, detect_cow_in_hull

# Données d'exemple
entities = [
    ("drone_1", 0, 0),
    ("drone_2", 10, 0), 
    ("drone_3", 5, 10),
    ("cows_1", 3, 3)
]

# Analyse complète avec le service
hull, has_cows, detected_cows = DroneService.analyze_perimeter(entities)

# Surveillance avec alerte automatique
DroneService.monitor_and_alert(entities)

# Utilisation des modules individuels
hull = convex_hull(entities)
has_cows, cows = detect_cow_in_hull(hull)
```

### Utilisation avec rétrocompatibilité

```python
# L'ancien code continue de fonctionner
from drone import convex_hull, detect_cow_in_hull, alert

entities = [("drone_1", 0, 0), ("drone_2", 10, 0), ("cows_1", 3, 3)]

hull = convex_hull(entities)
alert(hull)
```

## 📊 Format des données

Les entités sont représentées par des tuples `(entity_id, x, y)` :
- **entity_id** : Identifiant de l'entité (ex: "drone_1", "cows_2")
- **x, y** : Coordonnées dans le plan 2D

### Conventions de nommage
- **Drones** : ID contenant "drone" (ex: "drone_1", "drone_alpha")
- **Vaches** : ID contenant "cows" (ex: "cows_1", "cows_beta")

## 🔧 Exemples d'utilisation

### Exemple 1 : Surveillance basique
```python
from drone import DroneService

# Définir les positions
positions = [
    ("drone_1", 0, 0),
    ("drone_2", 10, 0),
    ("drone_3", 5, 10),
    ("cows_1", 3, 3),
    ("cows_2", 15, 5)  # Vache à l'extérieur
]

# Surveillance automatique
DroneService.monitor_and_alert(positions)
# Sortie: "ALERTE: Vache(s) détectée(s) dans l'enveloppe convexe"
#         " - Vache ID: cows_1, Position: (3, 3)"
```

### Exemple 2 : Analyse détaillée
```python
from drone import convex_hull, detect_cow_in_hull

# Calculer l'enveloppe convexe
hull = convex_hull(positions)
print(f"Enveloppe formée par: {hull}")

# Analyser la présence de vaches
has_cows, detected_cows = detect_cow_in_hull(hull)
if has_cows:
    print(f"Vaches détectées: {len(detected_cows)}")
    for cow in detected_cows:
        print(f"  - {cow[0]} à la position ({cow[1]}, {cow[2]})")
```

## 🧪 Tests et validation

Pour tester le module :
```python
# Test avec différentes configurations
test_cases = [
    # Cas 1: Pas de vaches
    [("drone_1", 0, 0), ("drone_2", 10, 0), ("drone_3", 5, 10)],
    
    # Cas 2: Vache à l'intérieur
    [("drone_1", 0, 0), ("drone_2", 10, 0), ("drone_3", 5, 10), ("cows_1", 3, 3)],
    
    # Cas 3: Vache à l'extérieur
    [("drone_1", 0, 0), ("drone_2", 10, 0), ("drone_3", 5, 10), ("cows_1", 15, 15)]
]

for i, entities in enumerate(test_cases, 1):
    print(f"\n--- Test {i} ---")
    DroneService.monitor_and_alert(entities)
```

## 📈 Algorithme

Le module utilise l'**algorithme d'Andrew** pour calculer l'enveloppe convexe :
1. Tri des points par coordonnées (x, y)
2. Construction de la partie basse de l'enveloppe
3. Construction de la partie haute de l'enveloppe
4. Fusion des deux parties

**Complexité** : O(n log n) où n est le nombre d'entités.

## 🔄 Migration depuis l'ancien code

Si vous utilisez l'ancien module `drone.py` :

```python
# Ancien code (continue de fonctionner)
from drone import convex_hull, alert
hull = convex_hull(entities)
alert(hull)

# Nouveau code (recommandé)
from drone import DroneService
DroneService.monitor_and_alert(entities)
```

## 🚨 Notes importantes

- Les ID des vaches doivent contenir le mot "cows" pour être détectées
- Les coordonnées sont en nombres flottants ou entiers
- Le module gère automatiquement les cas avec moins de 3 points
- La détection se base sur l'appartenance à l'enveloppe convexe, pas sur l'intérieur géométrique strict

## 📋 Variables d'environnement pour chaque drone

Chaque service drone accepte les variables d'environnement suivantes :

- **`DRONE_ID`** : Identifiant unique du drone (ex: "1", "2", "3", "4")
- **`DRONE_START_LAT`** : Latitude de la position de départ (ex: "46.9131")  
- **`DRONE_START_LNG`** : Longitude de la position de départ (ex: "-71.2085")
- **`DRONE_RADIUS`** : Rayon de couverture en mètres (ex: "800")
- **`MQTT_BROKER`** : Adresse du broker MQTT (ex: "mqtt-broker")

## 🐳 Configuration Docker Compose

Exemple de configuration dans `docker-compose.yaml` :

```yaml
services:
  drone1:
    build:
      context: ./drone
    environment:
      - DRONE_ID=1
      - MQTT_BROKER=mqtt-broker
      - DRONE_START_LAT=46.9131
      - DRONE_START_LNG=-71.2085
      - DRONE_RADIUS=800
    command: ["python", "-u", "drone_subscriber.py"]
  
  # Pas de service centralisé - chaque drone est autonome !
```

## 📡 Topics MQTT

- **`drones/positions`** : Positions individuelles des drones
- **`drones/zone`** : Zone de surveillance globale calculée
- **`vaches/positions`** : Positions des vaches (reçu par les drones)

## 🔄 Comportement Décentralisé des Drones

1. **Patrouille autonome** : Chaque drone effectue une patrouille circulaire autour de sa position de départ
2. **Mouvement coordonné** : Tous les drones se déplacent lentement vers l'ouest 
3. **Publication continue** : Chaque drone publie sa position toutes les 3 secondes
4. **Écoute collaborative** : Chaque drone écoute les positions des autres drones
5. **Leadership automatique** : Le drone avec l'ID le plus bas devient leader et calcule la zone
6. **Calcul distribué** : Chaque drone peut calculer la zone globale en cas de besoin
7. **Résilience** : Si le leader tombe, un autre drone prend automatiquement le relais

## 🎯 Avantages du Système Décentralisé

- **Pas de point de défaillance unique** : Aucun service centralisé critique
- **Auto-organisation** : Les drones s'organisent automatiquement
- **Résilience** : Fonctionne même si certains drones tombent
- **Scalabilité** : Facile d'ajouter/retirer des drones à la volée
- **Leadership dynamique** : Election automatique du leader basée sur l'ID
