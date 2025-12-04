"""
Module de détection et d'alerte pour les vaches.

Ce module contient les fonctions nécessaires pour détecter la présence de vaches
dans l'enveloppe convexe formée par les drones et générer les alertes appropriées.
"""


def detect_cow_in_hull(hull):
    """
    Détecte la présence de vaches dans l'enveloppe convexe.
    
    Args:
        hull: liste de tuples (entity_id, x, y) formant l'enveloppe convexe
        
    Returns:
        tuple: (booléen, liste de tuples (entity_id, x, y))
            - bool: True si au moins une vache est à l'intérieur de l'enveloppe
            - liste: liste des vaches à l'intérieur de l'enveloppe
    """
    inside_cows = [hull_point for hull_point in hull if "cows" in hull_point[0]]
    return len(inside_cows) > 0, inside_cows


def print_alert(cows):
    """
    Affiche les informations d'alerte pour les vaches détectées.
    
    Args:
        cows: liste de tuples (entity_id, x, y) représentant les vaches détectées
    """
    print("ALERTE: Vache(s) détectée(s) dans l'enveloppe convexe")
    for cow in cows:
        print(f" - Vache ID: {cow[0]}, Position: ({cow[1]}, {cow[2]})")


def alert(hull):
    """
    Vérifie la présence de vaches dans l'enveloppe convexe et affiche une alerte si nécessaire.
    
    Args:
        hull: liste de tuples (entity_id, x, y) formant l'enveloppe convexe
    """
    has_cow, cows = detect_cow_in_hull(hull)
    if has_cow:
        print_alert(cows)
    else:
        print("Toutes les vaches sont à l'extérieur, pas de repositionnement nécessaire.")
