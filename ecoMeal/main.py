import pandas as pd
import numpy as np
import math
import random

from ecoMeal.simplexe import calculate_meal_quantities_for_user_needs
from ecoMeal.user import user_information
from ecoMeal.user import get_user_needs
from ecoMeal.output_menu import generate_output
from ecoMeal.load import load_data
from ecoMeal.ecoscore import ecoscore_per_meal

def main():

    ingredients_data = load_data()

    print("\033[0;32mBienvenue dans ecoMeal, le générateur de repas personnalisés !\033[0m")

    user, number_of_meals, ecoscore_importance = user_information()
    needs = get_user_needs(user)

    print("Génération des repas en cours ...")

    best_ecoscore_value = math.inf
    worst_ecoscore_value = 0
    best_ecoscore_meal = None
    worst_ecoscore_meal = None

    for meal in ingredients_data.all_possible_meals:
        meal.quantities = calculate_meal_quantities_for_user_needs(meal.get_matrix(), needs)
        meal_ecoscore = ecoscore_per_meal(meal, meal.quantities)
        meal.ecoscore = meal_ecoscore

        if meal_ecoscore < best_ecoscore_value:
            best_ecoscore_value = meal_ecoscore
            best_ecoscore_meal = meal
        if meal_ecoscore > worst_ecoscore_value:
            worst_ecoscore_value = meal_ecoscore
            worst_ecoscore_meal = meal

    ecoscore_interval = worst_ecoscore_value - best_ecoscore_value
    ecoscore = ["A", "B", "C", "D", "E"]

    valid_meals = [] # liste de tous les repas correspondant au choix de l'utilisateur

    for meal in ingredients_data.all_possible_meals:
        meal_ecoscore_index = math.floor((((meal.ecoscore-best_ecoscore_value)*100)/ecoscore_interval)/20)
        if meal_ecoscore_index == 5:
            meal_ecoscore_index = 4 # pour le worst_ecoscore_meal, le floor donne 5, qui n'est pas dans la range 0 - 4 de la liste ecoscore
        meal.ecoscore_letter = ecoscore[meal_ecoscore_index]
        if meal_ecoscore_index <= ecoscore_importance:
            valid_meals.append(meal)

    if len(valid_meals)==0:
        print("Aucun repas ne correspond aux critères environnementaux et à vos besoins")
        return

    dataframe_list=[]

    if number_of_meals >= len(valid_meals):
        chosen_meal = valid_meals
    else :
        chosen_meal = random.sample(valid_meals, number_of_meals)


    for i, meal in enumerate(chosen_meal):

        print(f"Repas {i+1} : somme des écoscores = {meal.ecoscore:.2f}")
        print("Composition du repas :")

        for ingredient, qty in zip(meal.ingredients, meal.quantities):
            print(f"  - {ingredient.name} : {qty:.2f} unités, écoscore = {ingredient.ecoscore}")

        dataframe_list.append(generate_output(meal, meal.quantities))

    with pd.ExcelWriter("output/repas.xlsx") as writer:
        for i in range(len(dataframe_list)):
            dataframe_list[i].to_excel(writer, sheet_name=f"repas {i+1}", index=False)
    print("Fichier Excel généré avec succès !, dans ../output/repas.xlsx")

if __name__ == "__main__":
    main()
