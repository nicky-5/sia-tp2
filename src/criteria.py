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
    def __init__(self, delta: float):
        self.delta = delta

    def check(self, state: State):
        return False


# Content
class ContentCriteria:
    def __init__(self, max_generations: float, delta: float):
        self.max_generations = max_generations
        self.last = 0.0
        self.accum = 0
        self.delta = delta

    def check(self, state: State):
        best_of_last = max(state.generations[-1], key=lambda x: x.performance)
        if abs(best_of_last.performance - self.last) < self.delta:
            self.accum = 0
            self.last = best_of_last
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
