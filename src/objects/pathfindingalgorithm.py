from abc import ABC, abstractmethod
from typing import List

from PyQt5.QtCore import Qt

from src.objects.grid import Grid
from src.objects.rabbit import Rabbit
from src.objects.snake import Snake


class PathfindingAlgorithm(ABC):

    @abstractmethod
    def define_new_directions(
        self, grid: Grid, snake: Snake, rabbits: List[Rabbit]
    ) -> List[Qt.Key]:
        pass

    def __str__(self):
        return self.__class__.__name__
