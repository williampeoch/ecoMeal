import math
import pandas as pd
from functools import partial
from typing import List, Callable, Tuple
from random import choices, randint, randrange, random
from collections import namedtuple

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
Aliment = namedtuple('Aliment', ['name', 'kcal', 'prot', 'fat', 'carb'])

df = pd.read_excel("4-TableS1_augmented_with_FAO_data.xlsx").dropna()

aliments= []

grammes = [5, 50, 100, 250]
for index, row in df.iterrows():
    for i in range(len(grammes)):
        aliments.append(Aliment(row['Product'] + f" {grammes[i]}g", row['kcalPerRetailUnit'] * grammes[i]/1000, row['gProteinPerRetailUnit'] * grammes[i]/1000, row['gFatPerRetailUnit'] * grammes[i]/1000, row['gCarbPerRetailUnit'] * grammes[i]/1000))


def genome_to_aliments(genome: Genome, aliments: [Aliment]) -> [Aliment]:
    result = []
    for i, aliment in enumerate(aliments):
        if genome[i] == 1:
            result += [aliment.name]
    
    return result


def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)


def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]


def gaussian(x, mu, sigma):
    return math.exp(-((x - mu)**2) / (2 * sigma ** 2))

hist_fitness = []

def fitness(genome: Genome, aliments: [Aliment]) -> int:
    if len(genome) != len(aliments):
        raise ValueError("genome and aliments must be of the same length")
    
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

        if i > 50:
            with open('recipes.txt', 'a') as f:
                f.write(str(genome_to_aliments(population[0], aliments)) + "\n\n")

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


print(f"number of generations: {generations}")
print(f"best solution: {genome_to_aliments(population[0], aliments)}")


kcal_total = 0
prot_total = 0
fat_total = 0
carb_total = 0
for alim_string in genome_to_aliments(population[0], aliments):
    for aliment in aliments:
        if aliment.name == alim_string:
            kcal_total += aliment.kcal
            prot_total += aliment.prot
            fat_total += aliment.fat
            carb_total += aliment.carb

print(f"\nCIBLE : KCalories: 800, Prot: 25, Fat: 30, Carb: 100\n")
print(f"Repas: kcal: {kcal_total}, prot: {prot_total}, fat: {fat_total}, carb: {carb_total}")



import matplotlib.pyplot as plt
x_values = range(1, len(hist_fitness)+1)

plt.plot(x_values, hist_fitness)
plt.show()