import pandas as pd

def generate_output(meal, result_quantities):

    lines_list = []
    for i in range(len(result_quantities)):
        name = meal.ingredients[i].name
        quantity = result_quantities[i]
        lines_list.append([name, quantity])



    return pd.DataFrame(lines_list, columns=['Ingrédient', 'Quantités'])
