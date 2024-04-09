from src.functions import Character
from src.classes import Class
from heapq import heappush
import numpy as np

class_ = Class.ARCHER

characters = []

for strength in np.arange(0.0, 150.0, 0.5):
    for agility in np.arange(0, 150 - strength, 0.5):
        for proficiency in np.arange(0, 150 - strength - agility, 0.5):
            for resistance in np.arange(0, 150 - strength - agility - proficiency, 0.5):
                for health in np.arange(0, 150 - strength - agility - proficiency - resistance, 0.5):
                    for height in np.arange(1.3, 2.0, 0.1):
                        character = Character(
                            class_,
                            [strength, agility, proficiency, resistance, health],
                            height)
                        if character.performance > 50:
                            print(character.performance)
                            heappush(characters, character)
