import numpy 

class Meal:
	def __init__(self, ingredients):
		self.ingredients=ingredients



	def get_matrix(self):
		# self.ingredients = liste d'ingrédients pour le repas courant

		# matrice nb de col = len list
		# matrice nb de lignes = chacune des caractéristiques de l'ingrédient
		# numpy.matrix prend en paramètre une liste de liste
		# numpy.matrix([ligne 1, ligne 2, ligne 3])
		# ligne 1 à n: valeurs énergétique des ingrédients

		line_list=[]

		line_kcal=[]
		line_protein=[]
		line_fat=[]
		line_carb=[]

		for ingredient in self.ingredients:
			line_kcal.append(ingredient.kcal)
			line_protein.append(ingredient.protein)
			line_fat.append(ingredient.fat)
			line_carb.append(ingredient.carb)
		
		line_list.append(line_kcal)
		line_list.append(line_protein)
		line_list.append(line_fat)
		line_list.append(line_carb)
		
		return numpy.matrix(line_list)

