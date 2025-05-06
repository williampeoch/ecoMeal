from ecoMeal.type.person import Person
import re

def user_information():
    sex = get_input("Sexe (M/F) : ", "[MFmf]").upper()
    weight = float(get_input("Poids (kg) : ", "[0-9]+"))
    height = float(get_input("Taille (cm) : ", "[0-9]+"))
    age = int(get_input("Âge : ", "[0-9]+"))
    level_activity = get_input("Niveau d'activité (0 à 6) : ", "[0-6]")
    number_of_meals = int(get_input("Nombre de repas à générer ? ", "[1-9][0-9]*"))
    ecoscore_importance = get_ecoscore_importance()
    return Person(sex, weight, height, age, level_activity), number_of_meals, ecoscore_importance

def get_user_needs(user: Person):
    needs = user.get_nutritional_needs_per_meal()  # [protéines, lipides, glucides, kcal]
    
    print(f"\nBesoins pour ce repas : {needs[3]:.0f} kcal")
    print(f"Protéines : {needs[0]:.1f} g | Lipides : {needs[1]:.1f} g | Glucides : {needs[2]:.1f} g\n")
    
    return needs

def get_input(displayed_text, format):
    user_input = input(displayed_text)
    if re.search("^" + format + "$", user_input) != None:
        # le format est bon
        return user_input
    else:
        # le format est pas bon
        print("La valeur saisie est invalide.")
        return get_input(displayed_text, format)

def get_ecoscore_importance():
    while True:
        try:
            value = int(input("Sur une échelle de 1 (pas important) à 100 (très important), à quel point souhaitez-vous que vos repas respectent l'environnement ? "))
            if 1 <= value <= 100:
                return value
            else:
                print("Veuillez entrer un nombre entre 1 et 100.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre.")