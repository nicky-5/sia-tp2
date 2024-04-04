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

from heapq import heappush
from collections import defaultdict

import json


class Config:
    def __init__(self, config_file):
        # Read the JSON configuration from file
        with open(config_file, 'r') as f:
            config = json.load(f)

        # Assign configuration parameters to class attributes
        self.population_size = config["population_size"]
        self.mutation_rate = config["mutation_rate"]
        self.crossover_rate = config["crossover_rate"]
        self.max_generations = config["max_generations"]
        self.a = config["A"]
        self.selection_method_1 = config["selection_method_1"]
        self.selection_method_2 = config["selection_method_2"]
        self.a = config["B"]
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
    # 'ranking': raking
})

crossover_methods = defaultdict(lambda: single_point_crossover)
crossover_methods.update({
    'single_point': single_point_crossover,
    'double_point': double_point_crossover,
    'ring': ring_crossover,
    'uniform': uniform_crossover
})

if __name__ == "__main__":
    config_file = "config.json"
    config = Config(config_file)

    characters = []
    perf = []
    relative_fitness = []

    for i in range(1, config.population_size):
        character = Character.random(Class.ARCHER)
        heappush(perf, (character.performance(), character))
    total = sum(item[0] for item in perf)
    fitness = list(map(lambda pair: (pair[0]/total, pair[1]), perf))

    # print(perf)
    for item in fitness:
        print(item[0])
    final = elite(fitness, 10)
    print("\n\nAca esta el elite!\n\n")
    for item in final:
        print(item[0])

    print(fitness)

    print("roulette_selection")
    sel = roulette_selection(fitness, 10)
    print(sel)
    sel = boltzmann_selection(perf, 10)
    print("boltzmann_selection")
    print(sel)

    parent_1 = sel[0][1].get_allels()
    parent_2 = sel[2][1].get_allels()

    print(parent_1)
    print(parent_2)

    parent_1, parent_2 = crossover_methods[config.crossover_method](
        parent_1, parent_2)

    print(parent_1)
    print(parent_2)

    new = Character(Class.ARCHER, tuple(parent_1[0:5]), parent_1[-1])
    print("new points:", new.points)
    print("new height: ", new.height)
