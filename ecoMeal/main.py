import pandas as pd
import numpy as np
import math
import random

from ecoMeal.simplexe import calculate_meal_quantities_for_user_needs
from ecoMeal.user import user_information, get_user_needs
from ecoMeal.output_menu import generate_output
from ecoMeal.load import load_data
from ecoMeal.ecoscore import ecoscore_per_meal, get_valid_meals

def main():

    ingredients_data = load_data()

    print("\033[0;32mBienvenue dans ecoMeal, le générateur de repas personnalisés !\033[0m")

    user, number_of_meals, ecoscore_importance = user_information()
    needs = get_user_needs(user)

    print("Génération des repas en cours ...")



    valid_meals = get_valid_meals(ingredients_data, needs, ecoscore_importance)
    dataframe_list=[]

    if number_of_meals >= len(valid_meals):
        chosen_meal = valid_meals
        print("Le nombre de repas souhaité dépasse le nombre de repas valides")
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
