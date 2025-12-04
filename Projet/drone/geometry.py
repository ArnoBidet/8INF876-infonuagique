"""
Module de calculs géométriques pour le drone.

Ce module contient les fonctions nécessaires pour calculer l'enveloppe convexe
d'un ensemble de points dans un plan 2D.
"""


def cross_product(o, a, b):
    """
    Calcule le produit vectoriel OA x OB.
    
    Args:
        o, a, b: tuples (entity_id, x, y) représentant des points
        
    Returns:
        float: Produit vectoriel. Positif = tourne à gauche, négatif = tourne à droite
    """
    # o, a, b = (id, x, y)
    return (a[1] - o[1]) * (b[2] - o[2]) - (a[2] - o[2]) * (b[1] - o[1])


def convex_hull(entities):
    """
    Calcule l'enveloppe convexe d'un ensemble d'entités en utilisant l'algorithme d'Andrew.
    
    Args:
        entities: liste de tuples (entity_id, x, y)
                 entity_id peut être une vache (cow_id) ou un drone (drone_id)
                 
    Returns:
        list: Liste des tuples (entity_id, x, y) formant l'enveloppe convexe dans l'ordre
    """
    # Moins de 3 points -> enveloppe = points eux-mêmes
    if len(entities) <= 1:
        return entities

    # Trier les points par x puis y
    entities = sorted(entities, key=lambda e: (e[1], e[2]))

    # Construire la partie basse de l'enveloppe
    lower = []
    for p in entities:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Construire la partie haute de l'enveloppe
    upper = []
    for p in reversed(entities):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Fusionner (sans le dernier point de chaque liste car doublons)
    return lower[:-1] + upper[:-1]
