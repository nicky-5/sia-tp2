from src.classes import Class
from src.functions import performance, print_points, random_character
from heapq import heappush

if __name__ == "__main__":
    points = (50, 50, 50, 0, 0)
    print_points(points)
    characters = []
    perf = []
    relative_fitness = []

    for i in range(1, 100):
        character = random_character(Class.ARCHER)
        heappush(perf, (performance(character.class_,
                                    character.points, character.height), character))
    total = sum(item[0] for item in perf)
    fitness = list(map(lambda pair: (pair[0]/total, pair[1]), perf))

    print(perf)
    print(fitness)
