import pandas as pd
import numpy as np

from ecoMeal.simplexe import calculate_meal_optim
from ecoMeal.user import user_information
from ecoMeal.user import get_user_needs
from ecoMeal.output_menu import generate_output
from ecoMeal.load import load_data

def main():

    ingredients_data = load_data()

    print("\033[0;32mBienvenue dans ecoMeal, le générateur de repas personnalisés !\033[0m")

    user, number_of_meals, ecoscore_importance = user_information()
    needs = get_user_needs(user)

    dataframe_list=[]

    for i in range(number_of_meals):
        meal = ingredients_data.generate_meal()
        ecoscore_vector = np.array([ingredient.ecoscore for ingredient in meal.ingredients])
        meal_quantity = calculate_meal_optim(meal.get_matrix(), needs, ecoscore_vector, ecoscore_importance)
        total_ecoscore = float(np.dot(ecoscore_vector, meal_quantity))

        print(f"Repas {i+1} : somme des écoscores = {total_ecoscore:.2f}")
        print("Composition du repas :")

        for ingredient, qty in zip(meal.ingredients, meal_quantity):
            print(f"  - {ingredient.name} : {qty:.2f} unités, écoscore = {ingredient.ecoscore}")

        dataframe_list.append(generate_output(meal, meal_quantity))

    with pd.ExcelWriter("output/repas.xlsx") as writer:
        for i in range(len(dataframe_list)):
            dataframe_list[i].to_excel(writer, sheet_name=f"repas {i+1}", index=False)
    print("Fichier Excel généré avec succès !")

if __name__ == "__main__":
    main()
