import random
import numpy as np
from typing import List
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from src.objects.pathfindingalgorithm import PathfindingAlgorithm
from src.objects.traininghandler import TrainingHandler
from src.objects.grid import Grid
from src.objects.rabbit import Rabbit
from src.objects.snake import Snake
from src.objects.performancetracker import PerformanceTracker
from src.utils.constants import height, nb_lapins, width
from src.utils.utils import create_rabbits

ACTION_MAP = {0: Qt.Key_Up, 1: Qt.Key_Down, 2: Qt.Key_Left, 3: Qt.Key_Right}
REVERSE_ACTION_MAP = {v: k for k, v in ACTION_MAP.items()}


class GameEngine(QObject):
    game_won = pyqtSignal()
    game_lost = pyqtSignal()
    game_stop = pyqtSignal()

    def __init__(self, snake: Snake, rabbits: List[Rabbit], grid: Grid,
                 algorithm: PathfindingAlgorithm):
        super().__init__()
        self.snake = snake
        self.rabbits = rabbits
        self.grid = grid
        self.directions = []
        self.performance_tracker = PerformanceTracker()
        self.training_handler = TrainingHandler()
        self.algorithm = algorithm

    def update(self):
        if not self.directions:
            if not self.rabbits:
                self.win()
            else:
                self.directions = self.algorithm.define_new_directions(
                    rabbits=self.rabbits, snake=self.snake, grid=self.grid)
        self.move_snake()
        self.check_collision()
        self.check_eat()
        self.grid.update(snake=self.snake, rabbits=self.rabbits)

    def check_collision(self):
        head = self.snake.get_head()
        x_head, y_head = head[0], head[1]
        if not (0 <= x_head < width()
                and 0 <= y_head < height()) or (head in self.snake.body[1:]):
            self.loose()

    def define_new_directions(self):
        state = self.get_state()
        action = self.training_handler.select_action(intial_state=state)
        self.directions = [action]

    def check_eat(self):
        head = self.snake.get_head()
        x_head, y_head = head[0], head[1]
        for rabbit_ in self.rabbits:
            if rabbit_.x == x_head and rabbit_.y == y_head:
                self.performance_tracker.increment_lapins_manges()
                self.rabbits.remove(rabbit_)
                self.snake.grow()

    def move_snake(self):
        if self.directions:
            new_direction = self.directions.pop(0)
            self.snake.change_direction(new_direction)
        self.snake.move()
        self.performance_tracker.increment_movements()

    def win(self):
        self.performance_tracker.save_performance()
        self.performance_tracker.reset()
        self.game_won.emit()
        self.reset()

    def loose(self):

        self.performance_tracker.save_performance()
        self.performance_tracker.reset()
        self.game_lost.emit()
        self.reset()

    def stop(self):
        self.game_stop.emit()

    def get_state(self):
        return np.array([node.kind for row in self.grid.nodes for node in row],
                        dtype=np.int8)

    def reset(self):
        self.snake.body = [(10, 10), (10, 11), (10, 12)]
        self.rabbits.clear()
        self.rabbits.extend(
            create_rabbits(width=width(),
                           height=height(),
                           nb_lapins=nb_lapins()))
