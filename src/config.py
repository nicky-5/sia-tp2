from src.classes import Class
from src.crossover import (single_point_crossover,
                           double_point_crossover,
                           ring_crossover,
                           uniform_crossover)
from src.selection import (
    elite_selection,
    roulette_selection,
    boltzmann_selection,
    universal_selection,
    tournament_prob,
    ranking,
    tournament_det)
from src.mutation import multi_gene_mutation, gene_mutation
from src.replacement import traditional_replacement, youth_favoured_replacement

import json
from collections import defaultdict


class Config:
    def __init__(self, config_file):
        # Read the JSON configuration from file
        with open(config_file, 'r') as f:
            config = json.load(f)

        # Assign configuration parameters to class attributes
        self.population_size = config["population_size"]
        self.population_class = config["population_class"]
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
        self.boltzmann_temperature_start = config["boltzmann_temperature_start"]
        self.boltzmann_temperature_end = config["boltzmann_temperature_end"]
        self.boltzmann_temperature_constant = config["boltzmann_temperature_constant"]
        self.end_criteria = config["end_criteria"]
        self.max_generations = config["max_generations"]
        self.content_criteria_limit = config["content_criteria_limit"]
        self.content_criteria_delta = config["content_criteria_delta"]
        self.structure_criteria_stats_delta = config["structure_criteria_stats_delta"]
        self.structure_criteria_similar_gen_threshold = config["structure_criteria_similar_gen_threshold"]
        self.structure_criteria_individual_prop = config["structure_criteria_individual_prop"]
        self.end_delta = config["end_delta"]
        self.min_fitness = config["min_fitness"]


population_class = defaultdict(lambda: Class.ARCHER)
population_class.update({
    'ARCHER': Class.ARCHER,
    'WARRIOR': Class.WARRIOR,
    'DEFENDER': Class.DEFENDER,
    'INFILTRATOR': Class.INFILTRATOR,
})

selection_methods = defaultdict(lambda: elite_selection)
selection_methods.update({
    'elite': elite_selection,
    'roulette': roulette_selection,
    'universal': universal_selection,  # TODO
    'boltzmann': boltzmann_selection,
    'tournament_det': tournament_det,
    'tournament_prob': tournament_prob,
    'ranking': ranking     # TODO
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
