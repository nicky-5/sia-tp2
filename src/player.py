HEIGHT_MIN = 1.3
HEIGHT_MAX = 2.0

def atk_modifier(height: float) -> float:
    return 0.5 - (3*height - 5)*4 + (3*height - 5)*2 + height/2

def def_modifier(height: float) -> float:
    return 2 + (3*height - 5)*4 - (3*height - 5)*2 - height/2


def attack(strength: float, agility: float, proficiency: float, atk_mod: float) -> float:
    return (agility + proficiency) * strength * atk_mod

def defense(proficiency: float, resistance: float, health: float, def_mod: float) -> float:
    return (resistance + proficiency) * health * def_mod
