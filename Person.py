class Person:
    def __init__(self, sex, weight, height, age, level_activity):
        self.sex = sex
        self.weight = weight
        self.height = height
        self.age = age
        self.level_activity = level_activity

    def calculate_PAL(self):
        # Physical Activity Level
        PAL_values = {'0': 1.2, '1': 1.4, '2': 1.5, '3': 1.7, '4': 1.8, '5': 2.1, '6': 2.4}
        return PAL_values[self.level_activity]
    
    def calculate_BMR(self):
        # Calculate Basal Metabolic Rate with Mifflin-St Jeor Equation
        if self.sex == "male":
            return 10*self.weight + 6.25*self.height - 5*self.age + 5
        else:
            return 10*self.weight + 6.25*self.height - 5*self.age - 161
        
    def calculate_needs(self):
        # Calculate daily caloric needs
        BMR = self.calculate_BMR()
        PAL = self.calculate_PAL()
        daily_calories = BMR * PAL
        
        # Calculate macronutrient needs (in grams)
        # Proteins: 15-20% of total calories (using 17.5%)
        # Fats: 20-35% of total calories (using 27.5%)
        # Carbs: remaining calories (55%)
        protein_calories = daily_calories * 0.175
        fat_calories = daily_calories * 0.275
        carb_calories = daily_calories * 0.55
        
        # Convert calories to grams
        # Proteins: 4 calories per gram
        # Fats: 9 calories per gram
        # Carbs: 4 calories per gram
        protein_grams = protein_calories / 4
        fat_grams = fat_calories / 9
        carb_grams = carb_calories / 4
        
        return {
            'calories': round(daily_calories),
            'protein': round(protein_grams),
            'fat': round(fat_grams),
            'carb': round(carb_grams)
        }