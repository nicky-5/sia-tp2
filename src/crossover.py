import random
import math
from src.functions import Allels


# Single Point Crossover
def single_point_crossover(parent_1: Allels, parent_2: Allels) -> (Allels, Allels):
    print("single_point_crossover")
    length = len(Allels)
    crossover_point = random.randint(0, length)
    print("DEBUG: crossover_point: ", crossover_point)

    for i in range(crossover_point, length):
        print("DEBUG: i: ", i)
        aux = parent_1[i]
        parent_1[i] = parent_2[i]
        parent_2[i] = aux
    return (parent_1, parent_2)


# Double Point Crossover
def double_point_crossover(parent_1: Allels, parent_2: Allels) -> (Allels, Allels):
    length = len(Allels)
    crossover_point_1 = random.randint(0, length)
    crossover_point_2 = random.randint(crossover_point_1, length)
    print(crossover_point_1)
    print(crossover_point_2)

    for i in range(crossover_point_1, crossover_point_2):
        aux = parent_1[i]
        parent_1[i] = parent_2[i]
        parent_2[i] = aux
    return (parent_1, parent_2)


# Ring Crossover
def ring_crossover(parent_1: Allels, parent_2: Allels) -> (Allels, Allels):
    length = len(Allels)
    crossover_point = random.randint(0, length)
    segment = random.randint(0, math.ceil(length/2.0))

    print(crossover_point)
    print(segment)

    for i in range(0, segment):
        point = (crossover_point + i) % (length)
        print("POINT: ", point)
        aux = parent_1[point]
        parent_1[point] = parent_2[point]
        parent_2[point] = aux
    return (parent_1, parent_2)


# Uniform Crossover
def uniform_crossover(parent_1: Allels, parent_2: Allels, prob=0.5) -> (Allels, Allels):
    length = len(Allels)

    for i in range(0, length):
        rand = random.uniform(0, 1)
        if rand < prob:
            print("changed: ", i, "rand: ", rand)
            aux = parent_1[i]
            parent_1[i] = parent_2[i]
            parent_2[i] = aux
    return (parent_1, parent_2)
