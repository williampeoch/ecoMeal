from ecoMeal.simplexe import calculate_meal
from ecoMeal.user import user_information
from ecoMeal.user import get_user_needs
from ecoMeal.output_menu import generate_output
from ecoMeal.load import load_data
import pandas as pd 

def main():
    ingredients_data = load_data()

    
    print("Bienvenue dans ecoMeal, le générateur de repas personnalisés !")
   
    user, number_of_meals = user_information()
    needs = get_user_needs(user)
    
    dataframe_list=[]
    for i in range(number_of_meals):
        meal = ingredients_data.generate_meal()
        meal_quantity = calculate_meal(meal.get_matrix(), needs)
        dataframe_list.append(generate_output(meal, meal_quantity))

    with pd.ExcelWriter("output\\repas.xlsx") as writer:
        for i in range(len(dataframe_list)):
            dataframe_list[i].to_excel(writer, sheet_name=f"repas {i+1}", index=False)


if __name__ == "__main__":
    main()
