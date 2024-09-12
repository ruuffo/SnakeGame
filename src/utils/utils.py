import random
from typing import List
from PyQt5.QtCore import Qt

from src.objects.node import Node
from src.objects.snake import Snake
from src.objects.rabbit import Rabbit


def choose_direction(start_node: Node, end_node: Node) -> Qt.Key:
    if end_node.x - start_node.x > 0:
        return Qt.Key_Right
    elif end_node.x - start_node.x < 0:
        return Qt.Key_Left
    elif end_node.y - start_node.y > 0:
        return Qt.Key_Down
    else:
        return Qt.Key_Up


def create_rabbits(width: int, height: int, n_rabbits: int,
                   snake: Snake) -> List[Rabbit]:
    rabbits_set = set()

    while len(rabbits_set) < n_rabbits:
        new_rabbit_pos = random.randrange(width), random.randrange(height)
        if not (new_rabbit_pos in snake.body):
            rabbit = Rabbit(new_rabbit_pos[0], new_rabbit_pos[1])
            rabbits_set.add(rabbit)
    return list(rabbits_set)
