from functions import Character
from functions import performance
import random
# Elite

# Ruleta




def __roulette(population: list[Character], selection_amount: int) -> list[Character]:
    total_perf = sum(performance(character.class_,character.points,character.height) for character in population)
    
    cumulative_probs = []
    cumulative_prob = 0.0

    for character in population:
        #prob relativa de la selection al char
        prob = performance(character.class_,character.points,character.height) / total_perf
        
        # agrego la prob a la lista
        cumulative_prob =+ prob
        cumulative_probs.append(cumulative_prob)

    selections = []

    for _ in range(selection_amount):
        random_val = random.random()

        selected = None
        for i,cumulative_prob in enumerate(cumulative_probs):
            if random_val <= cumulative_prob:
                selected = population[i]
                break

        if selected is not None:
            selections.append(selected)
    
    return selections

# Universal

# Boltzmann

# Torneos (ambas versiones)

# Ranking
