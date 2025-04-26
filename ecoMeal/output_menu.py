import pandas as pd 

def generate_output(meal, result_quantities):

	lines_list = []
	for i in range(len(result_quantities)):
		name = meal.ingredients[i].name
		quantity = result_quantities[i]
		lines_list.append([name, quantity])



	return pd.DataFrame(lines_list, columns=['Ingrédient', 'Quantités'])


	# 

	# # 6. Calcul des apports réels
    # apports = A @ x
    # labels = ["kcal", "Protein", "Fat", "Carb"]
    # # 7. Génération du tableau final
    # results = df.copy()
    # results["OptimalQuantity (g)"] = x

    # total_row = pd.DataFrame({
    #     "Product": ["TOTAL (achieved)"],
    #     "Type": [""],
    #     "kcal": [apports[0]],
    #     "Protein": [apports[1]],
    #     "Fat": [apports[2]],
    #     "Carb": [apports[3]],
    #     "OptimalQuantity (g)": [np.sum(x)]
    #     })

    # target_row = pd.DataFrame({
    #     "Product": ["TARGET"],
    #     "Type": [""],
    #     "kcal": [b[0]],
    #     "Protein": [b[1]],
    #     "Fat": [b[2]],
    #     "Carb": [b[3]],
    #     "OptimalQuantity (g)": [""]
    #     })

    # final_df = pd.concat([results, total_row, target_row], ignore_index=True)
    # final_df.to_excel("repas_optimisé.xlsx", index=False)

 
