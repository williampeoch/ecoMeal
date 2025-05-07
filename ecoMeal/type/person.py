class Person:

    def __init__(self, sex, weight, height, age, level_activity):
        self.sex = sex
        self.weight = weight  # en kg
        self.height = height  # en cm
        self.age = age
        self.level_activity = level_activity

    def calculate_PAL(self):
        # Physical Activity Level
        PAL_values = {'0': 1.2, '1': 1.4, '2': 1.5, '3': 1.7, '4': 1.8, '5': 2.1, '6': 2.4}
        return PAL_values[self.level_activity]

    def calculate_BMR(self):
        # Basal Metabolic Rate avec la formule de Mifflin-St Jeor
        if self.sex == "male":
            return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            return 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

    def calculate_daily_needs(self):
        return self.calculate_BMR() * self.calculate_PAL()

    def get_nutritional_needs_per_meal(self):
        kcal_day = self.calculate_daily_needs()
        kcal_per_meal = kcal_day * 0.35  # exemple pour un déjeuner (~35% de l'apport)

        # Répartition standard des macronutriments
        prot_kcal = 0.2 * kcal_per_meal
        fat_kcal = 0.30 * kcal_per_meal
        carb_kcal = 0.50 * kcal_per_meal

        # Conversion en grammes
        prot_g = prot_kcal / 4     # 1g protéines = 4 kcal
        fat_g = fat_kcal / 9       # 1g lipides = 9 kcal
        carb_g = carb_kcal / 4     # 1g glucides = 4 kcal

        return [prot_g, fat_g, carb_g, kcal_per_meal]
