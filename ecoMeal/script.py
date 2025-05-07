from ecoMeal.load import load_data

def bricolage():
    ingredients_data = load_data()

    print(ingredients_data.get_ingredient_details("Fish (farmed)").get_environmental_data('ghg_emissions'))
    print(" ")
    print(ingredients_data.get_ingredient_details("Bovine Meat (beef herd)").get_environmental_data('ghg_emissions'))

bricolage()