from enum import Enum
from dataclasses import dataclass


@dataclass
class ClassModifier:
    atk_weight: float
    def_weight: float


class Class(Enum):
    WARRIOR = ClassModifier(0.6, 0.4)
    ARCHER = ClassModifier(0.9, 0.1)
    DEFENDER = ClassModifier(0.1, 0.9)
    INFILTRATOR = ClassModifier(0.8, 0.3)


def performance(class_: Class, attack: float, defense: float) -> float:
    return class_.value.atk_weight * attack + class_.value.def_weight * defense
