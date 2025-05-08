import numpy as np

from ecoMeal.type.ingredients_data import IngredientData

def ecoscore_per_meal(meal, quantities):
    ecoscore_vector = np.array([ingredient.ecoscore for ingredient in meal.ingredients])
    # score total repas : quantité  ingrédient 1 * score de l'ingrédient (pondération indicateur1 * valeur indicateur6 par unité + ... + pondération indicateur6 * valeur indicateur6 par unité)
    #                    + ...
    #                 +   quantité  ingrédient 6 * score de l'ingrédient (pondération indicateur1 * valeur indicateur6 par unité + ... + pondération indicateur6 * valeur indicateur6 par unité)
    return float(np.dot(ecoscore_vector, quantities)) # score total repas 




# calcul de l'impact total par indicateur pour un repas :
# somme_pour_un_indicateur : indicateur * quantité de l'ingrédient






# meilleur repas : quantité  ingrédient + score de l'ingrédient

# normalisation de chaque indicateur
# valeur de référence = basé sur la moyenne de chaque indictateur pour l'ensemble des repas générés ? (au delà d'un certain seuil : 100)
#
# score normalisé de chaque indicateur : somme_pour_un_indicateur / valeur de référence
#
# calcul de l'écoscore global
# score global = score normalisé de chaque indicateur * pondération des indicateurs (optionnel, fixé à 1)
#
# Echelle pour attribuer un ecoscore normalisé de 1 à 5 (pour correspondre à la note de l'utilisateur) : 0 il s'en fout et skip juste
# <20e percentile 5
# 20-40e percentile 4
# 40-60e percentile 3
# 60-80e percentile 2
# >80e 1
#
# plus l'écoscore global est faible meilleur est le repas = note de 5
