import random
from typing import List
from PyQt5.QtCore import Qt

from src.objects.rabbit import Rabbit


def choose_direction(n1, n2):
    if n2.x - n1.x > 0:
        return Qt.Key_Right
    elif n2.x - n1.x < 0:
        return Qt.Key_Left
    elif n2.y - n1.y > 0:
        return Qt.Key_Down
    else:
        return Qt.Key_Up


def create_rabbits(width: int, height: int, nb_lapins: int) -> List[Rabbit]:
    rabbits_set = set()
    while len(rabbits_set) < nb_lapins:
        rabbit = Rabbit(random.randrange(width), random.randrange(height))
        rabbits_set.add(rabbit)
    return list(rabbits_set)
