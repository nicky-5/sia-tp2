from typing import List
from src.functions import Character
from src.selection import Population
from dataclasses import dataclass


@dataclass
class State:
    generations: [Population]
    gen_i: int


# Maximum Generations
class MaxGenerations:
    def __init__(self, max_generations: float):
        self.max_generations = max_generations

    def check(self, state: State):
        if state.gen_i < self.max_generations:
            return True
        else:
            return False


# Structure Criteria
class StructureCriteia:
    def __init__(self, delta: float, stats_delta: List[float],similar_gen_threshold: int, similar_individual_prop: float):
        self.delta = delta
        self.stats_delta = stats_delta
        self.similar_gen_threshold = similar_gen_threshold
        self.similar_individual_prop = similar_individual_prop
        self.current_gen = 0

    def check(self, state: State):
        def match(individual : Character, other_individual: Character) -> bool:
            i = 0
            for stats1, stats2 in zip(individual.get_allels(),other_individual.get_allels()):
                if(abs(stats1 - stats2) > self.stats_delta[i]):
                    return False
                i =+ 1
            return True

        similar_individuals = 0
        for individual in state.generations[-1]:
            for prev_individual in state.generations[-2]:
                if(match(individual,prev_individual)):
                    similar_individuals += 1
                    break

        if similar_individuals >= self.similar_individual_prop * len(state.generations[-1]):
            self.current_gen += 1
        else:
            self.current_gen = 0

        return self.current_gen >= self.similar_gen_threshold


# Content
class ContentCriteria:
    def __init__(self, max_generations: float, delta: float):
        self.max_generations = max_generations
        self.last = 0.0
        self.accum = 0
        self.delta = delta

    def check(self, state: State):
        best_of_last = max(state.generations[-1], key=lambda x: x.performance)
        if abs(best_of_last.performance - self.last) > self.delta:
            self.accum = 0
            self.last = best_of_last.performance
            return True
        if self.accum < self.max_generations:
            self.accum += 1
            return True
        return False


# Optimum Environment
class MinFitness:
    def __init__(self, min_fitness: float):
        self.min_fitness = min_fitness

    def check(self, state: State):
        best_of_last = max(state.generations[-1], key=lambda x: x.performance)
        if best_of_last.performance < self.min_fitness:
            return True
        else:
            return False
