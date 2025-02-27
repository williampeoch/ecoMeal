
class Person:
    def __init__(self, sex, weight, height, age, level_activity):
        self.sex = sex
        self.weight = weight
        self.height = height
        self.age = age
        self.level_activity = level_activity

    def calculate_NAP(self):
        NAP_values = {'0': 1.2, '1': 1.4, '2': 1.5, '3': 1.7, '4': 1.8, '5': 2.1, '6': 2.4}
        return NAP_values[self.level_activity]