import pandas as pd
import numpy as np

from scipy.optimize import minimize

def calculate_meal(A, nutritional_targets, ecoscore_vector, ecoscore_importance, lambda_=1.0):

    # Objectif nutritionnel pour un repas
    b = np.array([
    nutritional_targets[3],  # kcal
    nutritional_targets[0],  # protéines
    nutritional_targets[1],  # lipides
    nutritional_targets[2],  # glucides
    ])

    # Ajout de la pénalisation de l'écoscore
    A_aug = np.vstack([A, lambda_ * ecoscore_importance * ecoscore_vector])
    b_aug = np.append(b, [0])  # On veut minimiser l'écoscore total, donc cible = 0

    #5. Résolution du système (moindres carrés)
    x = np.linalg.lstsq(A_aug, b_aug, rcond=None)[0]

    x = np.maximum(x, 0)  # Quantités positives

    return x

def calculate_meal_optim(A, nutritional_targets, ecoscore_vector, ecoscore_importance):

    n = A.shape[1]

    def objective(x):
        return 10 * ecoscore_importance * np.dot(ecoscore_vector, x)
    # S'assurer que chaque ligne de A est un vecteur 1D
    kcal_vec = np.array(A[0]).flatten()
    prot_vec = np.array(A[1]).flatten()
    fat_vec = np.array(A[2]).flatten()
    carb_vec = np.array(A[3]).flatten()
    constraints = [
        {'type': 'ineq', 'fun': lambda x: np.dot(kcal_vec, x) - nutritional_targets[3] * 0.8},
        {'type': 'ineq', 'fun': lambda x: nutritional_targets[3] * 1.2 - np.dot(kcal_vec, x)},
        {'type': 'ineq', 'fun': lambda x: np.dot(prot_vec, x) - nutritional_targets[0] * 0.8},
        {'type': 'ineq', 'fun': lambda x: nutritional_targets[0] * 1.2 - np.dot(prot_vec, x)},
        {'type': 'ineq', 'fun': lambda x: np.dot(fat_vec, x) - nutritional_targets[1] * 0.8},
        {'type': 'ineq', 'fun': lambda x: nutritional_targets[1] * 1.2 - np.dot(fat_vec, x)},
        {'type': 'ineq', 'fun': lambda x: np.dot(carb_vec, x) - nutritional_targets[2] * 0.8},
        {'type': 'ineq', 'fun': lambda x: nutritional_targets[2] * 1.2 - np.dot(carb_vec, x)},
    ]
    bounds = [(0, None)] * n
    x0 = np.ones(n)
    result = minimize(objective, x0, bounds=bounds, constraints=constraints)
    if result.success:
        return result.x
    else:
        print('Optimisation échouée:', result.message)
        return np.zeros(n)
