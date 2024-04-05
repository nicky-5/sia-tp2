from src.functions import Allels
import random


# Gene Mutation
def gene_mutation(allels: Allels, mutation_rate: float, mutation_delta: float, gene: int = 0) -> Allels:
    rand = random.uniform(0, 1)
    if rand < mutation_rate:
        delta = random.uniform(-allels[gene], allels[gene]) * mutation_delta
        allels[gene] += delta
    return allels


# Multi-Gene Mutation
def multi_gene_mutation(allels: Allels, mutation_rate: float, mutation_delta: float) -> Allels:
    for gene in range(0, len(allels)):
        allels = gene_mutation(allels, mutation_rate, mutation_delta, gene)
    return allels


# Mutation Function
def mutate(
    uniform_mutation: bool,
    mutation_function: callable,
    allels: Allels,
    mutation_rate: float,
    mutation_delta: float,
    generation: int,
    gene: int = 0
) -> Allels:
    mut_div = 1
    if not uniform_mutation:
        # Mutation Decreases with each generation
        mut_div = generation

    if mutation_function == gene_mutation:
        return mutation_function(
            allels, mutation_rate/mut_div, mutation_delta/mut_div, gene)
    else:
        return mutation_function(
            allels, mutation_rate/mut_div, mutation_delta/mut_div)
