import random
from typing import List
import tensorflow as tf
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from src.objects.pathfindingalgorithm import PathfindingAlgorithm
from src.objects.grid import Grid
from src.objects.rabbit import Rabbit
from src.objects.snake import Snake
from src.objects.performancetracker import PerformanceTracker
from src.utils.utils import create_rabbits
import logging
import numpy as np


class GameEngine(QObject):
    game_won = pyqtSignal()
    game_lost = pyqtSignal()
    game_stop = pyqtSignal()
    ACTION_MAP = {
        0: Qt.Key_Up,
        1: Qt.Key_Down,
        2: Qt.Key_Left,
        3: Qt.Key_Right,
    }
    REVERSE_ACTION_MAP = {v: k for k, v in ACTION_MAP.items()}

    def __init__(
        self,
        snake: Snake,
        rabbits: List[Rabbit],
        grid: Grid,
        algorithm: PathfindingAlgorithm,
        one_rabbit_mode: bool = False,
    ):
        super().__init__()
        if len(rabbits) != 1 and one_rabbit_mode:
            raise ValueError(
                "If one_rabbit_mode is set to True, the length of rabbits list must be equal to 1"
            )

        self.snake = snake
        self.rabbits = rabbits
        self.n_rabbit = len(rabbits)
        self.grid = grid
        self.directions = []
        self.algorithm = algorithm
        self.one_rabbit_mode = one_rabbit_mode
        self.performance_tracker = PerformanceTracker(
            n_rabbits=self.n_rabbit,
            width=self.grid.width,
            height=self.grid.height,
            algorithm=str(algorithm),
        )
        self.initial_snake_position = snake.body

    def reset(self,
              random_grid_size: bool = False,
              random_n_rabbits: bool = False):
        if random_grid_size:
            self.grid.randomize_size()
        self.snake.body = self.initial_snake_position.copy()
        if random_n_rabbits:
            self.n_rabbit = random.randint(
                1, int(self.grid.width * self.grid.height * 0.3))

        self.rabbits.clear()
        self.rabbits.extend(
            create_rabbits(
                width=self.grid.width,
                height=self.grid.height,
                n_rabbits=self.n_rabbit,
                snake=self.snake,
            ))
        self.directions.clear()
        self.performance_tracker = PerformanceTracker(
            n_rabbits=self.n_rabbit,
            width=self.grid.width,
            height=self.grid.height,
            algorithm=str(self.algorithm),
        )

    def update(self):
        self.grid.update(snake=self.snake, rabbits=self.rabbits)

        if not self.rabbits and not self.one_rabbit_mode:
            self.win()

        if not self.directions:
            self.directions = self.algorithm.define_new_directions(
                rabbits=self.rabbits, snake=self.snake, grid=self.grid)

        self.move_snake()
        self.check_eat()
        self.check_collision()

    def check_collision(self):
        x_head, y_head = self.snake.get_head()
        head = self.snake.get_head()

        if not (0 <= x_head < self.grid.width
                and 0 <= y_head < self.grid.height):
            logging.info(
                f"Snake out of bounds: head position ({x_head}, {y_head})")
            self.loose()
            return True

        elif head in self.snake.body[1:]:
            logging.info(f"Snake collision with itself at {head}")
            self.loose()
            return True
        return False

    def check_eat(self):
        head = self.snake.get_head()
        x_head, y_head = head[0], head[1]
        for rabbit_ in self.rabbits:
            if rabbit_.x == x_head and rabbit_.y == y_head:
                self.performance_tracker.increment_lapins_manges()
                self.rabbits.remove(rabbit_)
                self.snake.grow()
                if self.one_rabbit_mode:
                    self.rabbits = create_rabbits(
                        width=self.grid.width,
                        height=self.grid.height,
                        n_rabbits=self.n_rabbit,
                        snake=self.snake,
                    )
                logging.info(f"Rabbit eaten at ({x_head}, {y_head})")
                return True
        return False

    def move_snake(self):
        if self.directions:
            new_direction = self.directions.pop(0)
            self.snake.change_direction(new_direction)
        else:
            logging.warning("No directions available, snake is not moving.")
        self.snake.move()
        self.performance_tracker.increment_movements()

    def win(self):
        self.performance_tracker.win = True
        self.performance_tracker.save_performance()
        self.game_won.emit()

    def loose(self):
        self.performance_tracker.save_performance()
        self.game_lost.emit()

    def stop(self):
        self.game_stop.emit()

    def get_state_tensor(self):
        state = [node.kind for row in self.grid.nodes for node in row]
        state_tensor = tf.convert_to_tensor(state)
        state_tensor = tf.cast(state_tensor, tf.int32)
        state_tensor = tf.reshape(state_tensor,
                                  [1, self.grid.height, self.grid.width, 1])
        return state_tensor

    def step(self, action):
        """This class is dedicated for the training of the ActorCritic model"""
        direction = self.ACTION_MAP[action]
        done = False
        self.grid.update(snake=self.snake, rabbits=self.rabbits)

        if not self.rabbits and not self.one_rabbit_mode:
            done = True

        if not self.directions:
            self.directions.append(direction)

        self.move_snake()

        reward = 1 if self.check_eat() else 0

        if self.check_collision():
            reward = -1
            done = True

        next_state = self.get_state_tensor()
        return (
            next_state.astype(np.int32),
            np.array(reward, np.int32),
            done.astype(np.bool),
        )

    def tf_step(self, action: tf.Tensor) -> List[tf.Tensor]:
        return tf.numpy_function(self.step, [action],
                                 [tf.int32, tf.int32, tf.bool])
