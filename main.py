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
Aliment = namedtuple('Aliment', ['name', 'kcal', 'prot', 'fat', 'carb'])

df = pd.read_excel("data/nutritional_data.xlsx").dropna()

aliments= []

grammes = [50, 100]
for index, row in df.iterrows():
    for i in range(len(grammes)):
        aliments.append(Aliment(row['Product'] + f" {grammes[i]}g", row['kcalPerRetailUnit'] * grammes[i]/1000, row['gProteinPerRetailUnit'] * grammes[i]/1000, row['gFatPerRetailUnit'] * grammes[i]/1000, row['gCarbPerRetailUnit'] * grammes[i]/1000))


def genome_to_aliments(genome: Genome, aliments: [Aliment]) -> [Aliment]:
    result = []
    for i, aliment in enumerate(aliments):
        if genome[i] == 1:
            result += [aliment.name]
    
    return result


def generate_genome(length: int):
    num_ones = randint(1, min(10, length))
    genome = num_ones * [1] + (length - num_ones) * [0]
    shuffle(genome)
    return genome


def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]


def gaussian(x, mu, sigma):
    return math.exp(-((x - mu)**2) / (2 * sigma ** 2))

hist_fitness = []

def fitness(genome: Genome, aliments: [Aliment]) -> int:
    if len(genome) != len(aliments):
        raise ValueError("genome and aliments must be of the same length")
    
    if genome.count(1) > 10:
        return 0
    
    prot = 0
    fat = 0
    carb = 0
    kcal = 0

    for i, aliment in enumerate(aliments):
        if genome[i] == 1:
            prot += aliment.prot
            fat += aliment.fat
            carb += aliment.carb
            kcal += aliment.kcal

    kcal_fitness = gaussian(kcal, 800, 1000)
    prot_fitness = gaussian(kcal, 25, 10000)
    fat_fitness = gaussian(kcal, 30, 10000)
    carb_fitness = gaussian(kcal, 100, 10000)

    hist_fitness.append((kcal_fitness + prot_fitness + fat_fitness + carb_fitness) / 4)
    
    return (kcal_fitness + prot_fitness + fat_fitness + carb_fitness) / 4


def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
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
    fitness_limit=2,
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



# import matplotlib.pyplot as plt
# x_values = range(1, len(hist_fitness)+1)

# plt.plot(x_values, hist_fitness)
# plt.show()

def macros(genome):
    kcal_total = 0
    prot_total = 0
    fat_total = 0
    carb_total = 0
    for alim_string in genome_to_aliments(genome, aliments):
        for aliment in aliments:
            if aliment.name == alim_string:
                kcal_total += aliment.kcal
                prot_total += aliment.prot
                fat_total += aliment.fat
                carb_total += aliment.carb
    return [kcal_total, prot_total, fat_total, carb_total]


def second_mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Population:
    mutated_population = []
    for _ in range(10000):
        original_genome = genome[:]
        for _ in range(num):
            index = randrange(len(original_genome))
            original_genome[index] = abs(original_genome[index] - 1)
        mutated_population.append(original_genome)
    
    clean_mutated_population = []
    for genome_mutated in mutated_population:
        # check calories
        if (macros(genome_mutated)[0] > 700) and macros(genome_mutated)[0] < 900 and (macros(genome_mutated)[1] > 10) and (macros(genome_mutated)[1] < 40) and (macros(genome_mutated)[2] > 10) and (macros(genome_mutated)[2]) < 60 and (macros(genome_mutated)[3]) > 50 and (macros(genome_mutated)[3]) < 150 and genome_mutated.count(1) <= 10:
            clean_mutated_population.append(genome_mutated)
         
    return clean_mutated_population


mutated_population = second_mutation(population[0], num=5, probability=1)

for i in range(len(mutated_population)):
    with open('recipes.txt', 'a') as f:
                f.write(str(i) + str(genome_to_aliments(mutated_population[i], aliments)) + "\n\n")

# print(f"Mutation solution: {genome_to_aliments(mutated_population[0], aliments)}")
# print(f"\nCIBLE : KCalories: 800, Prot: 25, Fat: 30, Carb: 100\n")
# print(f"Repas: kcal: {kcal_total}, prot: {prot_total}, fat: {fat_total}, carb: {carb_total}")