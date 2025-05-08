from ecoMeal.type.person import Person
from ecoMeal.utils import get_input

def user_information():
    sex = get_input("Sexe (M/F) : ", "[MFmf]").upper()
    weight = float(get_input("Poids (kg) : ", "[0-9]+"))
    height = float(get_input("Taille (cm) : ", "[0-9]+"))
    age = int(get_input("Âge : ", "[0-9]+"))
    level_activity = get_input("Niveau d'activité (0 à 6) : ", "[0-6]")
    number_of_meals = int(get_input("Nombre de repas à générer ? ", "[1-9][0-9]*"))
    ecoscore_importance = int(get_input("Sur une échelle de 1 (pas important) à 5 (très important), à quel point souhaitez-vous que vos repas respectent l'environnement ? ","[1-5]"))

    # 5 - ecoscore_importance car :
    # ecoscore_letter ordre croissant : A = 0 ... E = 4
    # or user donne : 1 pas important et 5 très important
    # il faut donc inverser l'input
    return (Person(sex, weight, height, age, level_activity), number_of_meals, (5-ecoscore_importance)) # renvoie un tuple contenant : personne, nombre de repas et importance de l'impact environnemental

def get_user_needs(user: Person):
    needs = user.get_nutritional_needs_per_meal()  # [protéines, lipides, glucides, kcal]

    print(f"\nBesoins pour ce repas : {needs[3]:.0f} kcal")
    print(f"Protéines : {needs[0]:.1f} g | Lipides : {needs[1]:.1f} g | Glucides : {needs[2]:.1f} g\n")

    return needs
