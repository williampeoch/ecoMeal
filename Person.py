
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
        return self.calculate_BMR() * self.calculate_PAL()