from src.selection import SelectionFunction, Population
from src.functions import Character

import math


# Traditional Replacement
def traditional_replacement(current_generation: Population,
                            children: Population,
                            method_3: SelectionFunction,
                            method_4: SelectionFunction,
                            gen_size: int,
                            b: int) -> list[Character]:
    method_3_size = math.floor(gen_size * b)
    method_4_size = gen_size - method_3_size
    population = []
    population.extend(current_generation)
    population.extend(children)

    new_population = []
    new_population.extend(method_3(population, method_3_size))
    new_population.extend(method_4(population, method_4_size))
    return new_population


# Youth Favoured Replacement
def youth_favoured_replacement(current_generation: Population,
                               children: Population,
                               method_3: SelectionFunction,
                               method_4: SelectionFunction,
                               gen_size: int,
                               b: int) -> list[Character]:
    new_size = gen_size - len(children)
    new_population = []
    new_population.extend(children)
    if new_size == 0:
        return new_population

    method_3_size = math.floor(new_size * b)
    method_4_size = gen_size - method_3_size

    population = []
    population.extend(current_generation)

    new_population.extend(method_3(population, method_3_size))
    new_population.extend(method_4(population, method_4_size))
    return new_population
