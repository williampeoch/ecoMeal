import numpy as np
import math

from ecoMeal.simplexe import calculate_meal_quantities_for_user_needs
from ecoMeal.type.ingredients_data import IngredientData

def ecoscore_per_meal(meal, quantities):
    ecoscore_vector = np.array([ingredient.ecoscore for ingredient in meal.ingredients])
    # score total repas : quantité  ingrédient 1 * score de l'ingrédient (pondération indicateur1 * valeur indicateur6 par unité + ... + pondération indicateur6 * valeur indicateur6 par unité)
    #                    + ...
    #                 +   quantité  ingrédient 6 * score de l'ingrédient (pondération indicateur1 * valeur indicateur6 par unité + ... + pondération indicateur6 * valeur indicateur6 par unité)
    return float(np.dot(ecoscore_vector, quantities)) # score total repas

def get_best_and_interval_ecoscore(ingredients_data, needs):
    best_ecoscore_value = math.inf
    worst_ecoscore_value = 0

    for i in reversed(range(len(ingredients_data.all_possible_meals))):
        meal = ingredients_data.all_possible_meals[i]
        meal.quantities = calculate_meal_quantities_for_user_needs(meal.get_matrix(), needs)

        # le else est executé uniquement si la boucle ne break pas
        for quantity in meal.quantities:
            if quantity == 0 :
                del ingredients_data.all_possible_meals[i]
                break
        else:
            meal_ecoscore = ecoscore_per_meal(meal, meal.quantities)
            meal.ecoscore = meal_ecoscore

            if meal_ecoscore < best_ecoscore_value:
                best_ecoscore_value = meal_ecoscore
            if meal_ecoscore > worst_ecoscore_value:
                worst_ecoscore_value = meal_ecoscore

    ecoscore_interval = worst_ecoscore_value - best_ecoscore_value

    return best_ecoscore_value, ecoscore_interval

def get_valid_meals(ingredients_data, needs, ecoscore_importance):
    valid_meals = [] # liste de tous les repas correspondant au choix de l'utilisateur
    best_ecoscore_value, ecoscore_interval = get_best_and_interval_ecoscore(ingredients_data, needs)
    ecoscore = ["A", "B", "C", "D", "E"]

    for meal in ingredients_data.all_possible_meals:
        meal_ecoscore_index = math.floor((((meal.ecoscore-best_ecoscore_value)*100)/ecoscore_interval)/20)
        if meal_ecoscore_index == 5:
            meal_ecoscore_index = 4 # pour le worst_ecoscore_meal, le floor donne 5, qui n'est pas dans la range 0 - 4 de la liste ecoscore
        meal.ecoscore_letter = ecoscore[meal_ecoscore_index]
        if meal_ecoscore_index <= ecoscore_importance:
            valid_meals.append(meal)
    return valid_meals
