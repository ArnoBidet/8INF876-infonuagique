"""
Module drone - Point d'entrée principal (rétrocompatibilité).

Ce module maintient l'interface originale tout en utilisant les nouveaux
modules refactorisés pour une meilleure organisation du code.

DEPRECATED: Ce module est conservé pour la rétrocompatibilité.
Utilisez plutôt les modules spécialisés :
- geometry.py pour les calculs géométriques
- cow_detection.py pour la détection de vaches
- drone_service.py pour le service principal
"""

from .geometry import convex_hull
from .cow_detection import detect_cow_in_hull, alert

# Les fonctions sont maintenant importées des modules spécialisés
# Ceci maintient la rétrocompatibilité avec l'ancien code

__all__ = ['convex_hull', 'detect_cow_in_hull', 'alert']


