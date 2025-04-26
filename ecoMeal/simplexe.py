import pandas as pd
import numpy as np

def calculate_meal(A, nutritional_targets):

    # 4. Objectif nutritionnel pour un repas
    b = np.array([
    nutritional_targets[3],  # kcal
    nutritional_targets[0],  # protéines
    nutritional_targets[1],  # lipides
    nutritional_targets[2],  # glucides
    ])

    #5. Résolution du système (moindres carrés)
    # AtA = A.T @ A # Matrice transposée de A multipliée par A
    # Atb = A.T @ b

    # try:
    #     x = np.linalg.solve(A, b)
    # except np.linalg.LinAlgError:


    #5. Résolution du système (moindres carrés)    
    x = np.linalg.lstsq(A, b, rcond=None)[0]

    x = np.maximum(x, 0)  # Quantités positives

    return x


    
