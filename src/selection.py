from src.functions import Character
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Elite

# Ruleta


def roulette_selection(population: list[(float, Character)], selection_amount: int) -> list[Character]:
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
            selections.append(selected)

    return selections


# Universal

# Boltzmann


def boltzmann_selection(perf, t: int):
    total = sum(np.exp(item[0] / t) for item in perf)
    fitness = list(
        map(lambda pair: (np.exp(pair[0]/t)/total, pair[1]), perf))
    sel = roulette_selection(fitness, t)
    return sel


def graph_selection(fitness: [(float, Character)], sel: [float, Character]):
    plt.rcParams['figure.dpi'] = 200
    y_values = [f[0] for f in fitness]
    y_values = sorted(y_values, reverse=True)
    print("y values")
    print(y_values)
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
    sns.scatterplot(x=selected_x_values, y=selected_y_values, color='red', marker='+',
                    label='Selection')  # Scatterplot for selected points (in red)

    plt.show()


# Torneos (ambas versiones)

# Ranking