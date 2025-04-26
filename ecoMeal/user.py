from ecoMeal.type.person import Person

def user_information():
    sex = input("Sexe (M/F) : ").strip().upper()
    weight = float(input("Poids (kg) : "))
    height = float(input("Taille (cm) : "))
    age = int(input("Âge : "))
    level_activity = input("Niveau d'activité (0 à 6) : ")
    number_of_meals = int(input("Nombre de repas à générer ?"))
    return Person(sex, weight, height, age, level_activity), number_of_meals

def get_user_needs(user: Person):
    needs = user.get_nutritional_needs_per_meal()  # [protéines, lipides, glucides, kcal]
    
    print(f"\nBesoins pour ce repas : {needs[3]:.0f} kcal")
    print(f"Protéines : {needs[0]:.1f} g | Lipides : {needs[1]:.1f} g | Glucides : {needs[2]:.1f} g\n")
    
    return needs