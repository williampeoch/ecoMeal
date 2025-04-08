import numpy as np
import pandas as pd

# Charger l'Excel : df = pd.read_excel(nom_fichier, sheet_name=nom_feuille)
# Vérifier l'importation : print(df.head())
# nb : le retailUnit du fichier excel est en grammes ou mL

# Charger l'Excel
df = pd.read_excel("data/nutritional_data.xlsx", sheet_name="datas")

# Supposons que les colonnes sont : Product, Type, kcal, protein, fat, carb
# On ne garde que les colonnes numériques (sans "Product" et "Type")
A = df.iloc[:, 2:].T.to_numpy() # Prend seulement les colonnes kcal, protein, fat, carb

# Vecteur des besoins nutritionnels (second membre des contraintes)
b = np.array([1800, 45, 60, 200])

# Coefficients de la fonction objectif (on cherche à minimiser la quantité totale)
c = np.ones(A.shape[1]) # Minimiser la somme des ingrédients (on pourrait affiner)

## résolution de probleme d'optimisation lineaire
def simplex(c, A, b):
    """
    Implémente la méthode du simplexe pour résoudre un problème d'optimisation linéaire.
    min c^T x
    sous contraintes : Ax = b, x >= 0
    c : coeffciciant de la fonction objectif : c^T x
    A : matrice des coeffc   ients de contraintes
    b : second membre des contraintes : Ax = b, x >= 0
    """
    # m : nombre de contraintes
    # n : nombre de variables de décision
    m, n = A.shape
    tableau = np.hstack([A, np.eye(m), b.reshape(-1, 1)])  # Ajout des variables d'écart
    base = list(range(n, n + m))  # Variables de base

    while True:
        # Étape 1 : Vérifier si optimal
        if np.all(c[:] >= 0): # condition d'arret
            break

        # Étape 2 : Choisir la variable entrante (colonne avec coût réduit minimum)
        col_entrée = np.argmin(c)

        # Étape 3 : Choisir la variable sortante (Règle du rapport minimal)
        ratios = tableau[:, -1] / tableau[:, col_entrée]
        ratios[tableau[:, col_entrée] <= 0] = np.inf  # Éviter division par 0 ou négatif
        ligne_sortie = np.argmin(ratios)

        if ratios[ligne_sortie] == np.inf:
            raise ValueError("Problème non borné")

        # Étape 4 : Pivot de Gauss
        pivot = tableau[ligne_sortie, col_entrée]
        tableau[ligne_sortie] /= pivot
        for i in range(m):
            if i != ligne_sortie:
                tableau[i] -= tableau[i, col_entrée] * tableau[ligne_sortie]

        # Mise à jour de la base
        base[ligne_sortie] = col_entrée

        # Mise à jour des coûts
        c -= c[col_entrée] * tableau[ligne_sortie]

    # Extraire la solution optimale
    x_opt = np.zeros(n)
    for i, var in enumerate(base):
        if var < n:
            x_opt[var] = tableau[i, -1]

    return x_opt, c[-1]  # Solution et valeur optimale

# Exemple de test
# Fonction objectif : initialement de 0
# Valeurs cibles des apports
# v1 : somme des xi.kcali, apport calorique journalier de reference
# v2 : proteines
# v3 : lipides
# v4 : glucides
print(A)
print(b)
print(simplex(c, A, b))
