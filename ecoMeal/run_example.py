from ecoMeal.load import load_data
from ecoMeal.user import get_user_needs
from ecoMeal.type.person import Person
from ecoMeal.type.meal import Meal
from ecoMeal.simplexe import calculate_meal_quantities_for_user_needs
# nb pour une échelle de 1 à 100, regex : "([1-9][0-9]?|(100))"

# "Algorithmics and computer programming" + Sustainability - Final exam - April 2023

# Exercise 1 : Sustainability (4 points)

# A restaurant proposes the following menu:
# Fresh tomato salad
# ***
# Beef
# OR
# Salmon
# served with roasted potatoes
# ***
# Oven baked apple

# We will assume that the salmon is farmed (because approximately 70% of salmon produced worldwide
# is farmed), that the tomato salad is composed of tomatoes and olive oil, and that the oven baked apple
# is coated with beet sugar.
ingredient_names_salmon_menu = ["Fish (farmed)", "Tomatoes", "Olive Oil", "Beet Sugar"]
ingredient_names_beef_menu = ["Bovine Meat (beef herd)", "Tomatoes", "Olive Oil", "Beet Sugar"]

personne_type = Person("F", 55, 170, 23, "2")
needs = personne_type.get_nutritional_needs_per_meal()

# 1.1 Using data from Poore and Nemecek (Science, 2018) and the program you built during the labs,
# verify the affirmation that the salmon option reduces the greenhouse gas emissions of the meal. If
# yes, by how many percents?

data = load_data()
meal_ingredients_beef = []

for ingredient_name in ingredient_names_beef_menu:
    ingredient = data.get_ingredient_details(ingredient_name)
    meal_ingredients_beef.append(ingredient)

meal_beef = Meal(meal_ingredients_beef)
quantity_beef = calculate_meal_quantities_for_user_needs(meal_beef.get_matrix(), needs)[0]
beef = data.get_ingredient_details("Bovine Meat (beef herd)")
beef_emissions = beef.ghg_emissions * quantity_beef

# -------------
meal_ingredients_salmon = []

for ingredient_name in ingredient_names_salmon_menu:
    ingredient = data.get_ingredient_details(ingredient_name)
    meal_ingredients_salmon.append(ingredient)

meal_salmon = Meal(meal_ingredients_salmon)
quantities_salmon= calculate_meal_quantities_for_user_needs(meal_salmon.get_matrix(), needs)

# Récupération des ingrédients à comparer
fish = data.get_ingredient_details("Fish (farmed)")

# Affichage des valeurs d’émissions de GES
fish_emission = fish.ghg_emissions # ou tout autre indicateur défini dans config.json
beef_emission = beef.ghg_emissions

print(f"GHG emissions - Fish (farmed): {fish_emission:.2f} kg CO2eq")
print(f"GHG emissions - Bovine Meat: {beef_emission:.2f} kg CO2eq")

# Calcul du pourcentage de réduction
reduction = (beef_emission - fish_emission) / beef_emission * 100
print(f"\nSalmon option reduces GHG emissions by {reduction:.2f}% compared to beef.")
