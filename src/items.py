from math import tanh

POINTS_SUM = 150.0


def strength(points: float) -> float:
    return 100 * tanh(0.01 * points)


def agility(points: float) -> float:
    return tanh(0.01 * points)


def proficiency(points: float) -> float:
    return 0.6 * tanh(0.01 * points)


def resistance(points: float) -> float:
    return tanh(0.01 * points)


def health(points: float) -> float:
    return 100 * tanh(0.01 * points)
