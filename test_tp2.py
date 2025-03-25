import pandas as pd

nom_fichier = "data/ecological_data.xlsx"
nom_feuille = "ecodata"

# Charger l'Excel
df = pd.read_excel(nom_fichier, sheet_name=nom_feuille)

# Vérifier l'importation
print("j'affiche l'entete" )
print(df.head())

# Afficher les colonnes après transformation
print(df.columns)
