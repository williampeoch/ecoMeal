import pandas as pd
import random

from ecoMeal.type.ingredient import Ingredient
from ecoMeal.type.meal import Meal

class IngredientData:
    def __init__(self, dictionary_ingredients, ingredient_by_type):
        self.dictionary_ingredients=dictionary_ingredients
        self.ingredient_by_type=ingredient_by_type
        self.all_possible_meals=[]

        for prot in self.ingredient_by_type["ProteinSource"]:
          for carb in self.ingredient_by_type["CarbSource"]:
            for fat in self.ingredient_by_type["FatSource"]:
              for veg in self.ingredient_by_type["Vegetable"]:
                for fruit in self.ingredient_by_type["Fruit"]:
                  for extra in self.ingredient_by_type["Extra"]:
                      ingredients=[prot, carb, fat, veg, fruit, extra]
                      self.all_possible_meals.append(Meal(ingredients))

    def get_ingredient_details(self, ingredient_name):
        return self.dictionary_ingredients[ingredient_name]
