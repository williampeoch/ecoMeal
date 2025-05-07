import pandas as pd
import random

from ecoMeal.type.ingredient import Ingredient
from ecoMeal.type.meal import Meal

class IngredientData:
    def __init__(self, dictionary_ingredients, ingredient_by_type):
        self.dictionary_ingredients=dictionary_ingredients
        self.ingredient_by_type=ingredient_by_type

    def generate_meal(self):
        meal_ingredients=[]
        for type, ingredients_list in self.ingredient_by_type.items():
            meal_ingredients.append(random.choice(ingredients_list))
        return Meal(meal_ingredients) 

    def get_ingredient_details(self, ingredient_name):
        return self.dictionary_ingredients[ingredient_name]
