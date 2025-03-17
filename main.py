import math
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

aliments = [
    # Onions & Leeks (valeurs pour 1000g : 370 kcal, 7g prot, 1g fat, 83.3g carb)
    Aliment("Onions & Leeks 5g",   1.85,  0.035, 0.005,  0.4165),
    Aliment("Onions & Leeks 10g",  3.7,   0.07,  0.01,   0.833),
    Aliment("Onions & Leeks 50g",  18.5,  0.35,  0.05,   4.165),
    Aliment("Onions & Leeks 100g", 37.0,  0.7,   0.1,    8.33),
    Aliment("Onions & Leeks 250g", 92.5,  1.75,  0.25,   20.825),

    # Bananas (valeurs pour 1000g : 600 kcal, 7g prot, 3g fat, 136.4g carb)
    Aliment("Bananas 5g",   3.0,  0.035, 0.015,  0.682),
    Aliment("Bananas 10g",  6.0,  0.07,  0.03,   1.364),
    Aliment("Bananas 50g",  30.0,  0.35,  0.15,   6.82),
    Aliment("Bananas 100g", 60.0,  0.7,   0.3,    13.64),
    Aliment("Bananas 250g", 150.0, 1.75,  0.75,   34.1),

    # Citrus Fruit (valeurs pour 1000g : 260 kcal, 5g prot, 2g fat, 55.6g carb)
    Aliment("Citrus Fruit 5g",   1.3,  0.025, 0.01,  0.278),
    Aliment("Citrus Fruit 10g",  2.6,  0.05,  0.02,  0.556),
    Aliment("Citrus Fruit 50g",  13.0, 0.25,  0.1,   2.78),
    Aliment("Citrus Fruit 100g", 26.0, 0.5,   0.2,   5.56),
    Aliment("Citrus Fruit 250g", 65.0, 1.25,  0.5,   13.9),

    # Tomatoes (valeurs pour 1000g : 170 kcal, 8g prot, 2g fat, 30.1g carb)
    Aliment("Tomatoes 5g",   0.85, 0.04,  0.01,   0.1505),
    Aliment("Tomatoes 10g",  1.7,  0.08,  0.02,   0.301),
    Aliment("Tomatoes 50g",  8.5,  0.4,   0.1,    1.505),
    Aliment("Tomatoes 100g", 17.0, 0.8,   0.2,    3.01),
    Aliment("Tomatoes 250g", 42.5, 2.0,   0.5,    7.525),

    # Root Vegetables (valeurs pour 1000g : 380 kcal, 9g prot, 2g fat, 81.6g carb)
    Aliment("Root Vegetables 5g",   1.9,  0.045, 0.01,  0.408),
    Aliment("Root Vegetables 10g",  3.8,  0.09,  0.02,  0.816),
    Aliment("Root Vegetables 50g",  19.0, 0.45,  0.1,   4.08),
    Aliment("Root Vegetables 100g", 38.0, 0.9,   0.2,   8.16),
    Aliment("Root Vegetables 250g", 95.0, 2.25,  0.5,   20.4),
]

def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)

def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]

def gaussian(x, mu, sigma):
    return math.exp(-((x - mu)**2) / (2 * sigma ** 2))

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

    kcal_fitness = gaussian(kcal, 800, 50)
    prot_fitness = gaussian(kcal, 25, 5)
    fat_fitness = gaussian(kcal, 30, 5)
    carb_fitness = gaussian(kcal, 100, 10)
    
    return (kcal_fitness + prot_fitness + fat_fitness + carb_fitness) / 4

def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    print(sum([fitness_func(genome) for genome in population]))
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
    generation_limit=100
)


def genome_to_aliments(genome: Genome, aliments: [Aliment]) -> [Aliment]:
    result = []
    for i, aliment in enumerate(aliments):
        if genome[i] == 1:
            result += [aliment.name]
    
    return result

print(f"number of generations: {generations}")
print(f"best solution: {genome_to_aliments(population[0], aliments)}")