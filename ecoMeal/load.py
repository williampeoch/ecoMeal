from ecoMeal.type.ingredients_data import IngredientData
from ecoMeal.type.ingredient import Ingredient
import pandas as pd 

def load_data()->IngredientData:
	# 1. Lire le fichier Excel
	df = pd.read_excel("data\\nutritional_data.xlsx")
	data = df.to_dict(orient='records')

	list_ingredient=[]

	for element in data:
		ingredient = Ingredient(
			element["Product"],
			element["Type"],
			element["kcal"],
			element["Protein"],
			element["Fat"],
			element["Carb"],
			element["RetailUnit"]		 
			)
		list_ingredient.append(ingredient)

	print(f"Chargé {len(list_ingredient)} ingrédients")

	ingredient_by_type = {}

	for element in list_ingredient:
		temp_list=ingredient_by_type.get(element.type, [])
		temp_list.append(element)
		ingredient_by_type[element.type]=temp_list

	return IngredientData(ingredient_by_type)

	# # 2. Nettoyer les données
	# cols = ["kcal", "Protein", "Fat", "Carb"]
	# for col in cols:
	#     df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

	# # 3. Construire la matrice A (4 lignes : kcal, Prot, Fat, Carb)
	# A = df[["kcal", "Protein", "Fat", "Carb"]].to_numpy().T