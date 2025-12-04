"""
Package drone - Services de surveillance par drone.

Ce package fournit les fonctionnalités nécessaires pour la surveillance
de vaches par un système de drones utilisant des calculs d'enveloppe convexe.
"""

from .geometry import convex_hull, cross_product
from .cow_detection import detect_cow_in_hull, alert, print_alert
from .drone_service import DroneService, get_convex_hull, check_cows_and_alert

__all__ = [
    # Géométrie
    'convex_hull',
    'cross_product',
    
    # Détection de vaches
    'detect_cow_in_hull',
    'alert',
    'print_alert',
    
    # Service drone
    'DroneService',
    
    # Rétrocompatibilité
    'get_convex_hull',
    'check_cows_and_alert'
]
