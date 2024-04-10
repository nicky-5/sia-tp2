from src.functions import print_points, Character
from src.crossover import (single_point_crossover,
                           double_point_crossover,
                           ring_crossover,
                           uniform_crossover)
from src.selection import (Population,
                           select
                           )
from src.mutation import mutate
from src.items import POINTS_SUM
from src.player import HEIGHT_MAX, HEIGHT_MIN
from src.criteria import (State,
                          MaxGenerations,
                          StructureCriteria,
                          MinFitness,
                          ContentCriteria)
from src.config import (Config,
                        population_class,
                        selection_methods,
                        crossover_methods,
                        replacement_method,
                        mutation_method
                        )

from heapq import heappush
from collections import defaultdict

import math
import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.rcParams['figure.dpi'] = 200


if __name__ == "__main__":
    config_file = "config.json"
    config = Config(config_file)

    criteria_method = defaultdict(
        lambda: MaxGenerations(config.max_generations))
    criteria_method.update({
        'max_generations': MaxGenerations(config.max_generations),
        'structure_criteria': StructureCriteria(config.structure_criteria_stats_delta, config.structure_criteria_similar_gen_threshold, config.structure_criteria_individual_prop),
        'content_criteria': ContentCriteria(config.content_criteria_limit, config.content_criteria_delta),
        'min_fitness': MinFitness(config.min_fitness)
    })

    generation_0 = []
    state = State([], 0)

    for i in range(1, config.population_size):
        character = Character.random(population_class[config.population_class])
        heappush(generation_0, character)

    state.generations.append(generation_0)

    plt.figure()
    sns.set_style("whitegrid")

    line, = plt.plot(
        [], [],
        marker='',
        markersize=2,
        linestyle='-',
        label='Best Performance')
    line_individuals, = plt.plot(
        [], [],
        marker='.',
        markersize=2,
        linestyle='')
    line_mean, = plt.plot(
        [], [],
        marker='',
        markersize=2,
        linestyle='-',
        label='Mean Performance')
    line_median, = plt.plot(
        [], [],
        marker='.',
        markersize=2,
        linestyle='-',
        label='Median Performance')
    plt.xlabel('Generation')
    plt.ylabel('Performance')

    # Set the axes limits
    plt.xlim(0, config.max_generations)
    plt.ylim(0, 65)
    plt.legend()

    best_performance_data = []
    individual_performance_data = []
    mean_performance_data = []
    median_performance_data = []

    def update_plot(gen_i, state):
        best_of_last = max(state.generations[-1], key=lambda x: x.performance)
        best_performance_data.append(best_of_last.performance)
        line.set_data(range(1, gen_i + 1), best_performance_data)

        individual_performances = [
            individual.performance for individual in state.generations[-1]]
        individual_performance_data.append(individual_performances)
        line_individuals.set_data(np.tile(range(1, gen_i + 1), (len(individual_performances), 1)).T.flatten(),
                                  np.array(individual_performance_data).flatten())
        mean_performance_data.append(np.mean(individual_performances))
        line_mean.set_data(range(1, gen_i + 1), mean_performance_data)
        median_performance_data.append(np.median(individual_performances))
        line_median.set_data(range(1, gen_i + 1), median_performance_data)

        plt.pause(0.1)  # Pause to update the plot
        return line,

    while criteria_method[config.end_criteria].check(state):
        # Parent Selection
        parents = []
        parent_k = math.floor(config.population_size * config.child_rate)
        parent_k = parent_k if parent_k % 2 == 0 else parent_k - 1

        selection_1_k = math.ceil(parent_k * config.a)
        selection_2_k = parent_k - selection_1_k

        parents = []

        temperature = config.boltzmann_temperature_start - \
            config.boltzmann_temperature_constant * state.gen_i
        if temperature < config.boltzmann_temperature_end:
            temperature = config.boltzmann_temperature_end

        parents.extend(select(
            selection_methods[config.selection_method_1], state.generations[state.gen_i], selection_1_k, temperature))
        parents.extend(select(
            selection_methods[config.selection_method_2], state.generations[state.gen_i], selection_2_k, temperature))

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
                state.gen_i + 1,
                config.gene_to_modify
            )

            child_2_allels = mutate(
                config.uniform_mutation,
                mutation_method[config.mutation_method],
                child_2_allels,
                config.mutation_rate,
                config.mutation_delta,
                state.gen_i + 1,
                config.gene_to_modify
            )

            # Normalization of Allels
            total_child_1 = sum(child_1_allels[0:5])
            child_1_points = [child * POINTS_SUM /
                              total_child_1 for child in child_1_allels[0:5]]
            total_child_2 = sum(child_2_allels[0:5])
            child_2_points = [child * POINTS_SUM /
                              total_child_2 for child in child_2_allels[0:5]]

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
            config.b,
            temperature
        )

        state.generations.append(new_gen)
        print("GENERATION:", state.gen_i + 1)
        best_of_last = max(state.generations[-1], key=lambda x: x.performance)
        print("BEST OF LAST: ", best_of_last)
        print("Best of Last performance: ", best_of_last.performance)
        print(sum(best_of_last.points))

        state.gen_i += 1
        update_plot(state.gen_i, state)

    plt.show()
    # print("LAST GENERATION: ", generations[-1])
    best_of_last = max(state.generations[-1], key=lambda x: x.performance)

    print("BEST OF LAST: ", best_of_last)
    print("Best of Last performance: ", best_of_last.performance)
    print(sum(best_of_last.points))

    best_of_all = max(
        (individual for generation in state.generations for individual in generation), key=lambda x: x.performance)
    print("BEST OF ALL: ", best_of_all)
    print("Best of ALL performance: ", best_of_all.performance)
    print(sum(best_of_all.points))
