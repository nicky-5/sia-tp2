from src.classes import Class
from src.functions import print_points, Character
from src.crossover import (single_point_crossover,
                           double_point_crossover,
                           ring_crossover,
                           uniform_crossover)
from src.selection import (elite,
                           roulette_selection,
                           boltzmann_selection,
                           tournament_prob,
                           tournament_det)
from src.replacement import traditional_replacement, youth_favoured_replacement

from heapq import heappush
from collections import defaultdict

import json
import math
import random


class Config:
    def __init__(self, config_file):
        # Read the JSON configuration from file
        with open(config_file, 'r') as f:
            config = json.load(f)

        # Assign configuration parameters to class attributes
        self.population_size = config["population_size"]
        self.child_rate = config["child_rate"]
        self.mutation_rate = config["mutation_rate"]
        self.max_generations = config["max_generations"]
        self.a = config["A"]
        self.selection_method_1 = config["selection_method_1"]
        self.selection_method_2 = config["selection_method_2"]
        self.b = config["B"]
        self.replacement_method = config["replacement_method"]
        self.replacement_selection_method_1 = config["replacement_selection_method_1"]
        self.replacement_selection_method_2 = config["replacement_selection_method_2"]
        self.crossover_method = config["crossover_method"]


selection_methods = defaultdict(lambda: elite)
selection_methods.update({
    'elite': elite,
    'roulette': roulette_selection,
    # 'universal': universal_selection, # TODO
    'boltzmann': boltzmann_selection,
    'tournament_det': tournament_det,
    'tournament_prob': tournament_prob,
    # 'ranking': raking     # TODO
})

crossover_methods = defaultdict(lambda: single_point_crossover)
crossover_methods.update({
    'single_point': single_point_crossover,
    'double_point': double_point_crossover,
    'ring': ring_crossover,
    'uniform': uniform_crossover
})

replacement_method = defaultdict(lambda: youth_favoured_replacement)
crossover_methods.update({
    'youth_favoured': youth_favoured_replacement,
    'traditional': traditional_replacement
})


if __name__ == "__main__":
    config_file = "config.json"
    config = Config(config_file)
    generations = []
    generation_0 = []

    for i in range(1, config.population_size):
        character = Character.random(Class.ARCHER)
        heappush(generation_0, (character.performance(), character))

    generations.append(generation_0)

    for gen_i in range(0, config.max_generations):
        # Parent Selection
        parents = []
        parent_k = math.floor(config.population_size * config.child_rate)
        parent_k = parent_k if parent_k % 2 == 0 else parent_k - 1
        print(parent_k)

        selection_1_k = math.ceil(parent_k * config.a)
        selection_2_k = parent_k - selection_1_k
        print("selection 1: ", selection_1_k)
        print("selection 2: ", selection_2_k)

        parents = []
        parents.extend(selection_methods[config.selection_method_1](
            generations[gen_i], selection_1_k))
        parents.extend(selection_methods[config.selection_method_2](
            generations[gen_i], selection_2_k))
        print("PARENTS: ", parents)

        # Parent Crossover
        random.shuffle(parents)
        print("parent len: ", len(parents))
        i = 0

        children = []
        while i < parent_k:
            child_1_allels, child_2_allels = crossover_methods[
                config.crossover_method](
                parents[i][1].get_allels(), parents[i + 1][1].get_allels())

            # Mutation of Allels

            # Normalization of Allels
            total_child_1 = sum(child_1_allels[0:5])
            child_1_points = [child * 150 / total_child_1 for child in child_1_allels[0:5]]
            total_child_2 = sum(child_2_allels[0:5])
            child_2_points = [child * 150 / total_child_2 for child in child_2_allels[0:5]]
            print(child_1_points)

            child_1 = Character(parents[i][1].class_, tuple(
                child_1_points), child_1_allels[-1])

            child_2 = Character(parents[i + 1][1].class_, tuple(
                child_2_points), child_2_allels[-1])

            heappush(children, (child_1.performance(), child_1))
            heappush(children, (child_2.performance(), child_2))
            i += 2

        new_gen = replacement_method[config.replacement_method](
            parents,
            children,
            selection_methods[
                config.replacement_selection_method_1],
            selection_methods[
                config.replacement_selection_method_2],
            config.population_size,
            config.b
        )

        generations.append(new_gen)
        print("GENERATION:", gen_i + 1)

    print("LAST GENERATION: ", generations[-1])
    best_of_last = max(generations[-1], key=lambda x: x[0])
    print("BEST OF LAST")
    print(best_of_last)
    print(sum(best_of_last[1].points))

    # characters = []
    # perf = []
    # relative_fitness = []

    # for i in range(1, config.population_size):
    #     character = Character.random(Class.ARCHER)
    #     heappush(perf, (character.performance(), character))
    # total = sum(item[0] for item in perf)
    # fitness = list(map(lambda pair: (pair[0]/total, pair[1]), perf))

    # # print(perf)
    # for item in fitness:
    #     print(item[0])
    # final = elite(fitness, 10)
    # print("\n\nAca esta el elite!\n\n")
    # for item in final:
    #     print(item[0])

    # print(fitness)

    # print("roulette_selection")
    # sel = roulette_selection(fitness, 10)
    # print(sel)
    # sel = boltzmann_selection(perf, 10)
    # print("boltzmann_selection")
    # print(sel)

    # parent_1 = sel[0][1].get_allels()
    # parent_2 = sel[2][1].get_allels()

    # print(parent_1)
    # print(parent_2)

    # parent_1, parent_2 = crossover_methods[config.crossover_method](
    #     parent_1, parent_2)

    # print(parent_1)
    # print(parent_2)

    # new = Character(Class.ARCHER, tuple(parent_1[0:5]), parent_1[-1])
    # print("new points:", new.points)
    # print("new height: ", new.height)
