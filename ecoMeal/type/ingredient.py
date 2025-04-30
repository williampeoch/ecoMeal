conversion_table = {"kg": 0.001, "hg": 0.01, "dag": 0.1, "g": 1, "dg": 10, "cg": 100, "mg": 1000, "µg": 1000000,
                    "kl": 0.000001, "hl": 0.00001, "dal": 0.0001, "l": 0.001, "dl": 0.01, "cl": 0.1, "ml": 1, "µl": 1000}

class Ingredient:
    def __init__(self, name, type, kcal, protein, fat, carb, retail_unit):
        self.name = name
        self.type = type
        
        conversion_rate = 1
        if retail_unit.lower() in conversion_table:
            conversion_rate = conversion_table[retail_unit.lower()]

        self.kcal = kcal * conversion_rate
        self.protein = protein * conversion_rate
        self.fat = fat * conversion_rate
        self.carb = carb * conversion_rate

        if retail_unit[-1:].lower() == 'l':
            self.retail_unit = 'ml'
        elif retail_unit[-1:].lower() == 'g':
            self.retail_unit = 'g'
        else:
            self.retail_unit = retail_unit

