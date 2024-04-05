from src.classes import Class
from src.functions import print_points, Character
from src.crossover import (single_point_crossover,
                           double_point_crossover,
                           ring_crossover,
                           uniform_crossover)
from src.selection import (elite_selection,
                           roulette_selection,
                           boltzmann_selection,
                           universal_selection,
                           tournament_prob,
                           tournament_det)
from src.mutation import mutate, multi_gene_mutation, gene_mutation
from src.replacement import traditional_replacement, youth_favoured_replacement
from src.items import POINTS_SUM
from src.player import HEIGHT_MAX, HEIGHT_MIN

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
        self.mutation_delta = config["mutation_delta"]
        self.mutation_method = config["mutation_method"]
        self.gene_to_modify = config["gene_to_modify"]
        self.uniform_mutation = config["uniform_mutation"]
        self.max_generations = config["max_generations"]
        self.a = config["A"]
        self.selection_method_1 = config["selection_method_1"]
        self.selection_method_2 = config["selection_method_2"]
        self.b = config["B"]
        self.replacement_method = config["replacement_method"]
        self.replacement_selection_method_1 = config["replacement_selection_method_1"]
        self.replacement_selection_method_2 = config["replacement_selection_method_2"]
        self.crossover_method = config["crossover_method"]


selection_methods = defaultdict(lambda: elite_selection)
selection_methods.update({
    'elite': elite_selection,
    'roulette': roulette_selection,
    'universal': universal_selection, # TODO
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
replacement_method.update({
    'youth_favoured': youth_favoured_replacement,
    'traditional': traditional_replacement
})

mutation_method = defaultdict(lambda: gene_mutation)
mutation_method.update({
    'gene': gene_mutation,
    'multi_gene': multi_gene_mutation
})


if __name__ == "__main__":
    config_file = "config.json"
    config = Config(config_file)
    generations = []
    generation_0 = []

    for i in range(1, config.population_size):
        character = Character.random(Class.ARCHER)
        heappush(generation_0, character)

    generations.append(generation_0)

    for gen_i in range(0, config.max_generations):
        # Parent Selection
        parents = []
        parent_k = math.floor(config.population_size * config.child_rate)
        parent_k = parent_k if parent_k % 2 == 0 else parent_k - 1

        selection_1_k = math.ceil(parent_k * config.a)
        selection_2_k = parent_k - selection_1_k

        parents = []
        parents.extend(selection_methods[config.selection_method_1](
            generations[gen_i], selection_1_k))
        parents.extend(selection_methods[config.selection_method_2](
            generations[gen_i], selection_2_k))

        # Parent Crossover
        random.shuffle(parents)
        i = 0

        children = []
        while i < parent_k:
            child_1_allels, child_2_allels = crossover_methods[
                config.crossover_method](
                parents[i].get_allels(), parents[i + 1].get_allels())

            # Mutation of Allels
            child_1_allels = mutate(
                config.uniform_mutation,
                mutation_method[config.mutation_method],
                child_1_allels,
                config.mutation_rate,
                config.mutation_delta,
                gen_i + 1,
                config.gene_to_modify
            )

            child_2_allels = mutate(
                config.uniform_mutation,
                mutation_method[config.mutation_method],
                child_2_allels,
                config.mutation_rate,
                config.mutation_delta,
                gen_i + 1,
                config.gene_to_modify
            )

            # Normalization of Allels
            total_child_1 = sum(child_1_allels[0:5])
            child_1_points = [child * POINTS_SUM / total_child_1 for child in child_1_allels[0:5]]
            total_child_2 = sum(child_2_allels[0:5])
            child_2_points = [child * POINTS_SUM / total_child_2 for child in child_2_allels[0:5]]

            def normalize_height(height):
                return max(HEIGHT_MIN, min(HEIGHT_MAX, height))
            child_1_heigth = normalize_height(child_1_allels[-1])
            child_2_heigth = normalize_height(child_2_allels[-1])

            child_1 = Character(parents[i].class_, tuple(
                child_1_points), child_1_heigth)

            child_2 = Character(parents[i + 1].class_, tuple(
                child_2_points), child_2_heigth)

            heappush(children, child_1)
            heappush(children, child_2)
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

    # print("LAST GENERATION: ", generations[-1])
    best_of_last = max(generations[-1], key=lambda x: x.performance)

    print("BEST OF LAST: ", best_of_last)
    print("Best of Last performance: ", best_of_last.performance)
    print(sum(best_of_last.points))

    best_of_all = max((individual for generation in generations for individual in generation), key=lambda x: x.performance)
    print("BEST OF ALL: ", best_of_all)
    print("Best of ALL performance: ", best_of_all.performance)
    print(sum(best_of_all.points))
