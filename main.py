import math
import pandas as pd
from functools import partial
from typing import List, Callable, Tuple
from random import choices, randint, randrange, random, shuffle
from collections import namedtuple

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
Aliment = namedtuple('Aliment', ['name', 'kcal', 'prot', 'fat', 'carb', 'grammes', 'eco_score'])

df = pd.read_excel("data/nutritional_data.xlsx").dropna()
df_eco = pd.read_excel("data/eco_data.xlsx")

aliments= []

grammes = [10, 25, 50, 100]
for index, row in df.iterrows():
    for i in range(len(grammes)):
        aliments.append(Aliment(row['Product'], row['kcalPerRetailUnit'] * grammes[i]/1000, row['gProteinPerRetailUnit'] * grammes[i]/1000, row['gFatPerRetailUnit'] * grammes[i]/1000, row['gCarbPerRetailUnit'] * grammes[i]/1000, grammes[i], df_eco.loc[index, 'Score'] * grammes[i]/1000))

def genome_to_aliments(genome: Genome, aliments: [Aliment]):
    result = []
    for i, aliment in enumerate(aliments):
        if genome[i] == 1:
            result += [f"{aliment.name} {aliment.grammes}g"]
    
    return result


def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)


def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]


def gaussian(x, mu, sigma):
    return math.exp(-((x - mu)**2) / (2 * sigma ** 2))

hist_fitness = []

def fitness(genome: Genome, aliments: [Aliment]) -> float:
    if len(genome) != len(aliments):
        raise ValueError("genome and aliments must be of the same length")
    
    kcal = 0
    prot = 0
    fat = 0
    carb = 0

    eco_score = 0

    for i, aliment in enumerate(aliments):
        if genome[i] == 1:
            kcal += aliment.kcal
            prot += aliment.prot
            fat += aliment.fat
            carb += aliment.carb
            eco_score += aliment.eco_score


    kcal_fitness = gaussian(kcal, 800, 1000)
    prot_fitness = gaussian(prot, 25, 100)
    fat_fitness = gaussian(fat, 30, 1000)
    carb_fitness = gaussian(carb, 100, 1000)

    return kcal_fitness * prot_fitness * fat_fitness * carb_fitness * math.exp(-eco_score/10)


def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    weights=[fitness_func(genome) for genome in population],
    weights = weights[0] if isinstance(weights, tuple) else weights # idk why but it return a tuple instead of a list
    if sum(weights) == 0:
        return choices(population, k=2)

    return choices(
        population=population,
        weights=weights,
        k=2
    )


def single_point_crossover(a: Genome, b:Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of same length")
    
    length = len(a)
    if length < 2:
        return a, b
    
    p = randint(1, length-1)
    return a[0:p] + b[p:], b[0:p] + a[p:]


def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
    return genome


def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: int,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,
        generation_limit: int = 100
) -> Tuple[Population, int]:
    population = populate_func()

    for i in range(generation_limit):
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )

        if fitness_func(population[0]) >= fitness_limit:
            break
        
        hist_fitness.append(fitness_func(population[0]))
        
        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    population = sorted(
        population,
        key=lambda genome: fitness_func(genome),
        reverse=True
    )

    return population, i


population, generations = run_evolution(
    populate_func=partial(
        generate_population, size=10, genome_length=len(aliments)
    ),
    fitness_func=partial(
        fitness, aliments=aliments
    ),
    fitness_limit=0.99,
    generation_limit=1000
)

# print(population[0])
# print(f"number of generations: {generations}")
# print(f"best solution: {genome_to_aliments(population[0], aliments)}")


# kcal_total = 0
# prot_total = 0
# fat_total = 0
# carb_total = 0
# for alim_string in genome_to_aliments(population[0], aliments):
#     for aliment in aliments:
#         if aliment.name == alim_string:
#             kcal_total += aliment.kcal
#             prot_total += aliment.prot
#             fat_total += aliment.fat
#             carb_total += aliment.carb

# print(f"\nCIBLE : KCalories: 800, Prot: 25, Fat: 30, Carb: 100\n")
# print(f"Repas: kcal: {kcal_total}, prot: {prot_total}, fat: {fat_total}, carb: {carb_total}")
# print(fitness(population[0], aliments))


# import matplotlib.pyplot as plt
# x_values = range(1, len(hist_fitness)+1)

# plt.plot(x_values, hist_fitness, linewidth=0.1)
# plt.show()



# SECOND MUTATION

def second_mutation(genome):
    mutated_population = []

    for i in range(10000):
        modified_genome = genome[:]
        for _ in range(10):
            index = randrange(len(modified_genome))
            modified_genome[index] = abs(modified_genome[index] - 1)
        mutated_population.append(modified_genome)
    
    return mutated_population


def calculate_macros(genome, aliments):
    kcal = 0
    prot = 0
    fat = 0
    carb = 0

    eco_score = 0

    for i, aliment in enumerate(aliments):
        if genome[i] == 1:
            kcal += aliment.kcal
            prot += aliment.prot
            fat += aliment.fat
            carb += aliment.carb
            eco_score += aliment.eco_score

    return {'kcal': kcal, 'prot': prot, 'fat': fat, 'carb': carb, 'eco_score': eco_score}


def select_second_mutations(mutated_population):
    selected_population = []

    for genome in mutated_population:
        genome_macros = calculate_macros(genome, aliments)
        if genome_macros['kcal'] > 700 and genome_macros['kcal'] < 900 and genome_macros['prot'] > 10 and genome_macros['prot'] < 50 and genome_macros['fat'] > 10 and genome_macros['fat'] < 40 and genome_macros['carb'] > 50 and genome_macros['carb'] < 150 and math.exp(-genome_macros['eco_score']/10) > 0.9:
            selected_population.append(genome)
            print(genome_macros['eco_score'])
    
    return selected_population


second_mutated_population = select_second_mutations(second_mutation(population[0]))

for i, genome in enumerate(second_mutated_population):
    with open('recipes.txt', 'a') as f:
        f.write(str(i) + str(genome_to_aliments(genome, aliments)) + "\n\n")









print(calculate_macros(population[0], aliments))
print(genome_to_aliments(population[0], aliments))





# def macros(genome):
#     kcal_total = 0
#     prot_total = 0
#     fat_total = 0
#     carb_total = 0
#     for alim_string in genome_to_aliments(genome, aliments):
#         for aliment in aliments:
#             if aliment.name == alim_string:
#                 kcal_total += aliment.kcal
#                 prot_total += aliment.prot
#                 fat_total += aliment.fat
#                 carb_total += aliment.carb
#             print(f"{aliment.name} n'est pas dans {alim_string}")
#     return [kcal_total, prot_total, fat_total, carb_total]


# def second_mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Population:
#     mutated_population = []
#     for _ in range(10):
#         original_genome = genome[:]
#         for _ in range(num):
#             index = randrange(len(original_genome))
#             original_genome[index] = abs(original_genome[index] - 1)
#         mutated_population.append(original_genome)
    
#     clean_mutated_population = []
#     for genome_mutated in mutated_population:
#         # check calories
#         if (macros(genome_mutated)[0] > 700) and macros(genome_mutated)[0] < 900 and (macros(genome_mutated)[1] > 10) and (macros(genome_mutated)[1] < 40) and (macros(genome_mutated)[2] > 10) and (macros(genome_mutated)[2]) < 60 and (macros(genome_mutated)[3]) > 50 and (macros(genome_mutated)[3]) < 150:
#             clean_mutated_population.append(genome_mutated)
         
#     return clean_mutated_population


# mutated_population = second_mutation(population[0], num=5, probability=1)

# for i in range(len(mutated_population)):
#     with open('recipes.txt', 'a') as f:
#                 f.write(str(i) + str(genome_to_aliments(mutated_population[i], aliments)) + "\n\n")
