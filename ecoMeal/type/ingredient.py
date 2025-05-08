conversion_table = {"kg": 0.001, "hg": 0.01, "dag": 0.1, "g": 1, "dg": 10, "cg": 100, "mg": 1000, "µg": 1000000,
                    "kl": 0.000001, "hl": 0.00001, "dal": 0.0001, "l": 0.001, "dl": 0.01, "cl": 0.1, "ml": 1, "µl": 1000}

class Ingredient:
    def __init__(self, name, type, kcal, protein, fat, carb, retail_unit, environmental_impact, ecoscore):
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

        self.environmental_impact = environmental_impact
        self.ecoscore = ecoscore

    def get_protein(self):
        return self.protein

    def get_kcal(self):
        return self.kcal

    def get_environmental_data(self, key):
        return self.environmental_impact[key]

    def __str__(self):
        desc = self.name + " (type: " + self.type + ") ||| Nutritional data per 1" + self.retail_unit + ": " + str(self.kcal) + " Kcal | " + str(self.protein) + " Prot. | " + str(self.fat) + " Fat | " + str(self.carb) + " Carb ||| Environmental data: "
        for element in self.environmental_impact:
            desc = desc + str(self.environmental_impact[element]) + " " + element + " | "
        return desc

    def __getattr__(self, name):
        """Permet l'accès direct aux clés de environmental_impact comme attributs."""
        if name in self.environmental_impact:
            return self.environmental_impact[name]
        raise AttributeError(f"'Ingredient' object has no attribute '{name}'")
