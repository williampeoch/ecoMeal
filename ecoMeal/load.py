import pandas as pd
import json

from ecoMeal.type.ingredients_data import IngredientData
from ecoMeal.type.ingredient import Ingredient
from ecoMeal.utils import convert_column_name_to_index

def load_data()->IngredientData:

    # Le fichier de configuration permet d'éviter d'avoir des noms codés en dur dans le code
    with open("config/config.json", 'r') as file:
        config = json.load(file)

    # Chargement des données
    nutri_config = config["nutritional_data"]
    nutri_df = pd.read_excel(
    nutri_config["file_path"],
    sheet_name=nutri_config["sheet_name"],
    header=nutri_config["header"]
    )

    eco_config = config["ecological_data"]
    eco_df = pd.read_excel(
    eco_config["file_path"],
    sheet_name=eco_config["sheet_name"],
    header=eco_config["header"]
    )

    # Créer la liste des colonnes à importer depuis eco_df
    eco_columns = [config["ecological_data"]["ingredient_column"]] + [i["column_index"] for i in config["ecological_data"]["indicateur"]]

    list_col_names = eco_df.columns
    ingredient_column_index = convert_column_name_to_index(config["ecological_data"]["ingredient_column"]["column_index"]) # récupération de l'index de la colonne qui contient les ingrédients dans l'Excel ecological_data

    # TODO:
    # eco_df = eco_df.rename(columns={ingredient_column_index: "Product"})
    # list_col_names = eco_df.columns
    ingredient_column_name = list_col_names[ingredient_column_index] # nom de la colonne qui contient les ingrédients dans l'Excel ecological_data
    col_list_extract = [ingredient_column_name] + [list_col_names[convert_column_name_to_index(element["column_index"])] for element in config["ecological_data"]["indicateur"]]
    # print(col_list_extract)

    subset_eco_df = eco_df[col_list_extract]
    # print(subset_eco_df)

    # Fusionner sur la colonne 'Product'
    nutri_df = nutri_df.merge(subset_eco_df, left_on=["Product"], right_on=[ingredient_column_name], how="left")
    # print(nutri_df)

    data = nutri_df.to_dict(orient='records')

    list_ingredient=[]
    dictionary_ingredients = {}

    for element in data:
        impact = {indicateur["ID"]: element.get(list_col_names[convert_column_name_to_index(indicateur["column_index"])], None) for indicateur in config["ecological_data"]["indicateur"]}
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
        dictionary_ingredients[element["Product"]] = ingredient
        list_ingredient.append(ingredient)

    print(f"Chargé {len(list_ingredient)} ingrédients")

    ingredient_by_type = {}

    for element in list_ingredient:
        temp_list=ingredient_by_type.get(element.type, [])
        temp_list.append(element)
        ingredient_by_type[element.type]=temp_list

    return IngredientData(dictionary_ingredients, ingredient_by_type)
