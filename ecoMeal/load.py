from ecoMeal.type.ingredients_data import IngredientData
from ecoMeal.type.ingredient import Ingredient
import pandas as pd
import json

def convert_column_name_to_index(column_name):
    column_name = column_name.upper()
    column_index = 0
    column_name_len = len(column_name)
    for index, col_char in enumerate(column_name):
        pow_index = column_name_len - 1 - index
        char_value = ord(col_char)-64 # la valeur ASCII de A = 65, or on veut A = 1 (format excel)
        real_char_value = char_value*pow(26, pow_index)
        column_index += real_char_value
    return column_index - 1 # excel est indexé à 1, column_index est indexé à 0


def load_data()->IngredientData:

    nutri_df = pd.read_excel("data/nutritional_data.xlsx")
    eco_df = pd.read_excel("data/ecological_data.xlsx", sheet_name = "Results - Retail Weight", header = 1)
    print(eco_df)

    with open("ecoMeal/config.json", 'r') as file:
        config = json.load(file)

    # Créer la liste des colonnes à importer depuis eco_df
    eco_columns = [config["ingredient_column"]] + [i["column_index"] for i in config["indicateur"]]

    list_col_names = eco_df.columns
    ingredient_column_index = convert_column_name_to_index(config["ingredient_column"]["column_index"]) # récupération de l'index de la colonne qui contient les ingrédients dans l'Excel ecological_data

    # TODO:
    # eco_df = eco_df.rename(columns={ingredient_column_index: "Product"})
    # list_col_names = eco_df.columns
    ingredient_column_name = list_col_names[ingredient_column_index] # nom de la colonne qui contient les ingrédients dans l'Excel ecological_data
    col_list_extract = [ingredient_column_name] + [list_col_names[convert_column_name_to_index(element["column_index"])] for element in config["indicateur"]]
    print(col_list_extract)
    subset_eco_df = eco_df[col_list_extract]
    print(subset_eco_df)

    # Fusionner sur la colonne 'Product'
    nutri_df = nutri_df.merge(subset_eco_df, left_on=["Product"], right_on=[ingredient_column_name], how="left")
    print(nutri_df)
    data = nutri_df.to_dict(orient='records')

    list_ingredient=[]

    for element in data:
        impact = {indicateur["ID"]: element.get(list_col_names[convert_column_name_to_index(indicateur["column_index"])], None) for indicateur in config["indicateur"]}
        ingredient = Ingredient(
            element["Product"],
            element["Type"],
            element["kcal"],
            element["Protein"],
            element["Fat"],
            element["Carb"],
            element["RetailUnit"],
            impact
        )
        list_ingredient.append(ingredient)

    print(f"Chargé {len(list_ingredient)} ingrédients")

    ingredient_by_type = {}

    for element in list_ingredient:
        temp_list=ingredient_by_type.get(element.type, [])
        temp_list.append(element)
        ingredient_by_type[element.type]=temp_list

    return IngredientData(ingredient_by_type)
