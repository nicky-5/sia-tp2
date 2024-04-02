from __future__ import annotations
import src.items as items
import src.player as player
import src.classes as classes
import random
import numpy as np

from src.classes import Class

PointsTuple = tuple[float, float, float, float, float]

STATS_FUNCTIONS = (
    items.strength,
    items.agility,
    items.proficiency,
    items.resistance,
    items.health
)


class Character:
    def __init__(self, class_: Class, points: PointsTuple, height: int):
        self.class_ = class_
        self.points = points
        self.height = height

    def __lt__(self, _: Character) -> bool:
        return False


def performance(class_: Class, item_points: PointsTuple, height: float) -> float:
    def apply_pair(pair): return pair[0](pair[1])

    stats = map(apply_pair, zip(STATS_FUNCTIONS, item_points, strict=True))
    strength, agility, proficiency, resistance, health = stats

    atk_modifier = player.atk_modifier(height)
    def_modifier = player.def_modifier(height)

    attack = player.attack(strength, agility, proficiency, atk_modifier)
    defense = player.defense(proficiency, resistance, health, def_modifier)

    return classes.performance(class_, attack, defense)


def random_character(class_: Class):
    height = random.uniform(player.HEIGHT_MIN, player.HEIGHT_MAX)
    s = np.zeros(5)

    while (sum(s) == 0.0):
        s = np.random.uniform(0, 1, 5)

    stats = items.POINTS_SUM * s / sum(s)

    return Character(class_, stats, height)


def print_points(items: PointsTuple):
    names = list(map(lambda func: func.__name__, STATS_FUNCTIONS))

    width = max(map(len, names))
    padded = map(lambda name: name.ljust(width), names)

    for name, points in zip(padded, items, strict=True):
        print("{} = {}".format(name, points))
