import numpy as np
import pandas as pd
from itertools import combinations, product

# Charger l'Excel
df = pd.read_excel("data/nutritional_data.xlsx", sheet_name="datas")

# Extraire les valeurs nutritionnelles
A = df.iloc[:, 2:].to_numpy() # kcal, protein, fat, carb
ingredients = df.iloc[:, 0].values # Liste des ingrédients

# Besoins nutritionnels
b = np.array([1800, 45, 60, 200])

# Générer des quantités possibles (de 0 à 300g par pas de 10g)
quantities = np.arange(0, 301, 10)

# Stocker les solutions valides
solutions = []

# Explorer des combinaisons d'ingrédients et quantités
for subset_size in range(1, min(6, len(ingredients) + 1)): # Taille des combinaisons d'ingrédients
    for ingredient_subset in combinations(range(len(ingredients)), subset_size):
        for quantity_comb in product(quantities, repeat=subset_size):
            x = np.zeros(len(ingredients)) # Initialiser un vecteur de quantités
            x[list(ingredient_subset)] = quantity_comb # Assigner les quantités aux ingrédients sélectionnés

            # Calculer l'apport nutritionnel
            nutrition = A.T @ x # Produit matriciel

            # Calculer l'erreur quadratique (moindres carrés)
            error = np.sum((nutrition - b) ** 2)

            # Accepter les solutions qui ne dépassent pas trop l'objectif
            if np.all(nutrition >= 0.8 * b) and np.all(nutrition <= 1.2 * b):
                solutions.append((x, error))

# Trier les solutions par erreur croissante
solutions.sort(key=lambda s: s[1])

# Afficher les 10 meilleures solutions
for i, (x, error) in enumerate(solutions[:10]):
    selected_ingredients = {ingredients[j]: x[j] for j in range(len(ingredients)) if x[j] > 0}
    print(f"Solution {i+1} (Erreur: {error:.2f}): {selected_ingredients}")
