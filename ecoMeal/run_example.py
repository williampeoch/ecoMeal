from ecoMeal.load import load_data
from ecoMeal.user import get_user_needs

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

meal = create_meal_from_names(data, ingredient_names)

# 1.1 Using data from Poore and Nemecek (Science, 2018) and the program you built during the labs,
# verify the affirmation that the salmon option reduces the greenhouse gas emissions of the meal. If
# yes, by how many percents?

data = load_data()

# Récupération des ingrédients à comparer
fish = data.get_ingredient_details("Fish (farmed)")
beef = data.get_ingredient_details("Bovine Meat (beef herd)")

# Affichage des valeurs d’émissions de GES
fish_emission = fish.ghg_emissions # ou tout autre indicateur défini dans config.json
beef_emission = beef.ghg_emissions

print(f"GHG emissions - Fish (farmed): {fish_emission:.2f} kg CO2eq")
print(f"GHG emissions - Bovine Meat: {beef_emission:.2f} kg CO2eq")

# Calcul du pourcentage de réduction
reduction = (beef_emission - fish_emission) / beef_emission * 100
print(f"\nSalmon option reduces GHG emissions by {reduction:.2f}% compared to beef.")

# Maintenant il faut faire ce calcul mais pour un repas, les besoins nutritionnels du repas seront ceux de l'utilisateur
user, number_of_meals, ecoscore_importance = user_information()
needs = get_user_needs(user)
