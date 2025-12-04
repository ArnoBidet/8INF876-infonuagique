"""
Service principal du drone.

Ce module orchestre les fonctionnalités du drone en utilisant les modules
de géométrie et de détection de vaches.
"""

from .geometry import convex_hull
from .cow_detection import alert, detect_cow_in_hull


class DroneService:
    """
    Service principal pour la gestion des opérations du drone.
    """
    
    @staticmethod
    def analyze_perimeter(entities):
        """
        Analyse le périmètre formé par les entités et vérifie la présence de vaches.
        
        Args:
            entities: liste de tuples (entity_id, x, y) représentant drones et vaches
            
        Returns:
            tuple: (enveloppe_convexe, a_des_vaches, vaches_detectees)
        """
        hull = convex_hull(entities)
        has_cows, detected_cows = detect_cow_in_hull(hull)
        
        return hull, has_cows, detected_cows
    
    @staticmethod
    def monitor_and_alert(entities):
        """
        Surveille les entités et déclenche une alerte si nécessaire.
        
        Args:
            entities: liste de tuples (entity_id, x, y) représentant drones et vaches
        """
        hull = convex_hull(entities)
        alert(hull)
        
        return hull


# Fonctions compatibles avec l'ancienne interface (pour rétrocompatibilité)
def get_convex_hull(entities):
    """Fonction de rétrocompatibilité pour convex_hull."""
    return convex_hull(entities)


def check_cows_and_alert(hull):
    """Fonction de rétrocompatibilité pour alert."""
    alert(hull)
