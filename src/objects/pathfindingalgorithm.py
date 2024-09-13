from abc import ABC, abstractmethod
import logging
import random
from typing import List

from PyQt5.QtCore import Qt

from src.objects.grid import Grid
from src.objects.rabbit import Rabbit
from src.objects.snake import Snake


class PathfindingAlgorithm(ABC):

    @abstractmethod
    def compute(self, grid: Grid, snake: Snake,
                rabbits: List[Rabbit]) -> List[Qt.Key]:
        pass

    def define_new_directions(self, grid: Grid, snake: Snake,
                              rabbits: List[Rabbit]) -> List[Qt.Key]:
        directions = self.compute(grid=grid, snake=snake, rabbits=rabbits)
        if not directions:
            directions = self.random_move(grid=grid, snake=snake)
        return directions

    def random_move(self, grid: Grid, snake: Snake) -> List[Qt.Key]:
        logging.warning(
            "No valid path found to the rabbit. Defaulting to random move.")
        random_possible_moves = snake.possible_moves(grid=grid)
        if random_possible_moves:

            return [random.choice(random_possible_moves)]
        else:
            return [
                random.choice(
                    [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right])
            ]

    def __str__(self):
        return self.__class__.__name__
