from typing import List
from PyQt5.QtCore import Qt
import tensorflow as tf
import numpy as np
from src.objects.grid import Grid
from src.objects.pathfindingalgorithm import PathfindingAlgorithm
from src.objects.rabbit import Rabbit
from src.objects.snake import Snake
from src.objects.actorcritic import ActorCritic


class ActorCriticAlgorithm(PathfindingAlgorithm):

    def __init__(self, model: ActorCritic) -> None:
        self.model = model
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.1)

    def define_new_directions(self, grid: Grid, snake: Snake,
                              rabbits: List[Rabbit]) -> List[Qt.Key]:
        return super().define_new_directions(grid, snake, rabbits)
