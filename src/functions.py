from __future__ import annotations
from dataclasses import dataclass

import numpy as np

import src.items as items
import src.player as player
import src.classes as classes

from src.classes import Class

PointsTuple = tuple[float, float, float, float, float]
Allels = [float, float, float, float, float, float]

STATS_FUNCTIONS = (
    items.strength,
    items.agility,
    items.proficiency,
    items.resistance,
    items.health
)


@dataclass(order=True)
class Character:
    class_: Class
    points: PointsTuple
    height: float

    def __init__(self, class_: Class, points: PointsTuple, height: float):
        self.class_ = class_
        self.points = points
        self.height = height

    def random(class_: Class) -> Character:
        height = np.random.uniform(player.HEIGHT_MIN, player.HEIGHT_MAX)
        array = np.random.uniform(0, 1, len(STATS_FUNCTIONS))

        if sum(array) == 0.0:
            array = np.ones(len(STATS_FUNCTIONS))

        points = items.POINTS_SUM * array / sum(array)

        return Character(class_, points, height)

    def performance(self) -> float:
        def apply_pair(pair): return pair[0](pair[1])

        stats = map(apply_pair, zip(STATS_FUNCTIONS, self.points, strict=True))
        strength, agility, proficiency, resistance, health = stats

        atk_modifier = player.atk_modifier(self.height)
        def_modifier = player.def_modifier(self.height)

        attack = player.attack(strength, agility, proficiency, atk_modifier)
        defense = player.defense(proficiency, resistance, health, def_modifier)

        return classes.performance(self.class_, attack, defense)

    def get_allels(self) -> Allels:
        allels = [
            self.points[0],
            self.points[1],
            self.points[2],
            self.points[3],
            self.points[4],
            self.height
        ]
        print("points: ", self.points)
        print("allels: ", allels)
        return allels


def print_points(items: PointsTuple):
    names = list(map(lambda func: func.__name__, STATS_FUNCTIONS))

    width = max(map(len, names))
    padded = map(lambda name: name.ljust(width), names)

    for name, points in zip(padded, items, strict=True):
        print("{} = {}".format(name, points))
