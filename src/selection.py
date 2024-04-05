import random
from src.classes import performance
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import copy
from src.functions import Character

from typing import Callable

Population = list[Character]
SelectionFunction = Callable[[Population, int], list[Character]]


# Elite
def elite_selection(population: Population, selection_amount: int) -> Population:
    total = sum(character.performance for character in population)
    fitness = list(map(lambda character: (character.performance/total, character), population))
    selection = sorted(fitness, reverse=True)[:selection_amount]
    return [sel[1] for sel in selection]


# Ruleta
def roulette_selection(population: Population, selection_amount: int) -> Population:
    total = sum(character.performance for character in population)
    fitness = list(map(lambda character: (character.performance/total, character), population))
    return roulette(fitness, selection_amount)


def roulette(population: Population, selection_amount: int) -> Population:
    cumulative_probs = []
    cumulative_prob = 0.0

    for tup in population:
        cumulative_probs.append((cumulative_prob + tup[0], tup))
        # agrego la prob a la lista
        cumulative_prob += tup[0]

    selections = []

    for _ in range(selection_amount):
        random_val = random.random()

        selected = None
        for i, cumulative_prob in enumerate(cumulative_probs):
            if random_val <= cumulative_prob[0]:
                selected = cumulative_prob[1]
                break

        if selected is not None:
            selections.append(selected[1])

    return selections

# Universal

# falta cambiar el r_j por el de universal, sigue igual a roullette


def universal_selection(population: Population, selection_amount: int) -> Population:
    total = sum(character.performance for character in population)
    fitness = list(map(lambda character: (character.performance/total, character), population))

    cumulative_probs = []
    cumulative_prob = 0.0

    for tup in fitness:
        cumulative_probs.append((cumulative_prob + tup[0]))
        # agrego la prob a la lista
        cumulative_prob += tup[0]

    selections = []
    random_init = random.random()
    j = 0

    for _ in range(selection_amount):
        random_value = (random_init + j) / selection_amount - 1
        j += 1

        # Encuentra el individuo correspondiente al valor aleatorio
        selected_individual = None
        for i, cumulative_prob in enumerate(cumulative_probs):
            if random_value <= cumulative_prob:
                selected_individual = fitness[i]
                break

        if selected_individual is not None:
            selections.append(selected_individual[1])
    return selections


# Boltzmann
def boltzmann_selection(population: Population, t: int) -> Population:
    total = sum(np.exp(character.performance / t) for character in population)
    fitness = list(
        map(lambda character: (np.exp(character.performance/t)/total, character), population))
    sel = roulette(fitness, t)
    return sel


def graph_selection(fitness: list[tuple[float, Character]], sel: list[float, Character]):
    plt.rcParams['figure.dpi'] = 200
    y_values = [f[0] for f in fitness]
    y_values = sorted(y_values, reverse=True)
    x_values = range(0, len(y_values))

    # Create scatterplot using Seaborn
    sns.scatterplot(x=x_values, y=y_values)
    plt.xlabel('X Values')
    plt.ylabel('Y Values')
    plt.title('Scatterplot of X and Y Values')

    selected_y_values = []
    selected_x_values = []

    for tup in sel:
        selected_y_values.append(tup[0])
        i = 0
        for y_val in y_values:
            if y_val == tup[0]:
                selected_x_values.append(i)
            i += 1
    sns.scatterplot(x=selected_x_values, y=selected_y_values, color='red',
                    marker='+', label='Selection')

    plt.show()


# Torneos (ambas versiones)
def tournament_det(population: Population, winners: int, participants: int = 10) -> Population:
    total = sum(item.performance for item in population)
    fitness = list(map(lambda character: (
        character.performance/total, character), population))

    # ret: list[Character] = list()
    ret = []

    for _ in range(winners):
        sample = random.choices(fitness, k=participants)
        winner = max(sample, key=lambda x: x[0])
        ret.append(winner[1])
    return ret


def tournament_prob(population: Population, winners: int, threshold: float = 0.8) -> Population:
    ret: list[Character] = list()
    total = sum(item.performance for item in population)
    fitness = list(map(lambda character: (
        character.performance/total, character), population))

    for _ in range(winners):
        sample = random.choices(fitness, k=2)
        selector = max if random.random() < threshold else min
        winner = selector(sample, key=lambda x: x[0])
        ret.append(winner[1])
    return ret

# Ranking
def ranking(population : Population,selection_amount : int) -> Population:
    total = sum(character.performance for character in population)
    ranked_list=list(map(lambda character: (character.performance/total, character), population))
    ranked_list = sorted(ranked_list,reverse=True)
    size = len(ranked_list)
    i = 0
    new_ranked_list = []
    for tup in ranked_list:
        new_ranked_list.append(((size - i)/size,tup[1]))
        i+=1
    return roulette(new_ranked_list,selection_amount)

    



