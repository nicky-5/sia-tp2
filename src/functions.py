import src.items as items
import src.player as player
import src.classes as classes

from src.classes import Class

PointsTuple = tuple[float, float, float, float, float]

STATS_FUNCTIONS = (
    items.strength,
    items.agility,
    items.proficiency,
    items.resistance,
    items.health
)

def performance(class_: Class, item_points: PointsTuple, height: float) -> float:
    apply_pair = lambda pair : pair[0](pair[1])

    stats = map(apply_pair, zip(STATS_FUNCTIONS, item_points, strict=True))
    strength, agility, proficiency, resistance, health = stats

    atk_modifier = player.atk_modifier(height)
    def_modifier = player.def_modifier(height)

    attack = player.attack(strength, agility, proficiency, atk_modifier)
    defense = player.defense(proficiency, resistance, health, def_modifier)

    return classes.performance(class_, attack, defense)

def print_points(items: PointsTuple):
    names = list(map(lambda func : func.__name__, STATS_FUNCTIONS))

    width = max(map(len, names))
    padded = map(lambda name : name.ljust(width), names)

    for name, points in zip(padded, items, strict=True):
        print("{} = {}".format(name, points))
