def convex_hull(entities):
    """
    entities : liste de tuples (entity_id, x, y)
    entity_id peut être une vache (cow_id) ou un drone(drone_id) (n'est pas utilisé pour le calcul)

    Retourne la liste (entity_id, x,y) formant l'enveloppe convexe dans l'ordre.
    """
    # Moins de 3 points -> enveloppe = points eux-mêmes
    if len(entities) <= 1:
        return entities

    # Trier les points par x puis y
    entities = sorted(entities, key=lambda e: (e[1], e[2]))

    def cross(o, a, b):
        """Produit vectoriel OA x OB. Positif = tourne à gauche."""
        # o, a, b = (id, x, y)
        return (a[1]-o[1])*(b[2]-o[2]) - (a[2]-o[2])*(b[1]-o[1])


    # Construire la partie basse de l'enveloppe
    lower = []
    for p in entities:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Construire la coque haute
    upper = []
    for p in reversed(entities):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Fusionner (sans le dernier point de chaque liste car doublons)
    return lower[:-1] + upper[:-1]

def detect_cow_in_hull(hull):
    """
    hull : liste de tuples (entity_id, x, y) formant l'enveloppe convexe

    return : (booléen, liste de tuples (entity_id, x, y))
        bool : True si au moins une vache est à l'intérieur de l'enveloppe
        liste de tuples : liste des vaches à l'intérieur de l'enveloppe
    """

    inside_cows = [hull_point for hull_point in hull if "cows" in hull_point[0]]
    return len(inside_cows) > 0, inside_cows

def alert(hull):
    """
    hull : liste de tuples (entity_id, x, y) formant l'enveloppe convexe

    Affiche une alerte si une vache est détectée dans l'enveloppe convexe.
    """

    has_cow, cows = detect_cow_in_hull(hull)
    if has_cow:
        print("ALERTE: Vache(s) détectée(s) dans l'enveloppe convexe")
        for cow in cows:
            print(f" - Vache ID: {cow[0]}, Position: ({cow[1]}, {cow[2]})")
    else:
        print("Toutes les vaches sont à l'intérieur, pas de repositionnement nécessaire.")


