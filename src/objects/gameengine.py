import random
import numpy as np
from typing import List
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from src.objects.pathfindingalgorithm import PathfindingAlgorithm
from src.objects.grid import Grid
from src.objects.rabbit import Rabbit
from src.objects.snake import Snake
from src.objects.performancetracker import PerformanceTracker
from src.utils.utils import create_rabbits


class GameEngine(QObject):
    game_won = pyqtSignal()
    game_lost = pyqtSignal()
    game_stop = pyqtSignal()

    def __init__(
        self,
        snake: Snake,
        rabbits: List[Rabbit],
        grid: Grid,
        algorithm: PathfindingAlgorithm,
    ):
        super().__init__()
        self.snake = snake
        self.rabbits = rabbits
        self.n_rabbit = len(rabbits)
        self.grid = grid
        self.directions = []
        self.algorithm = algorithm
        self.performance_tracker = PerformanceTracker(
            n_rabbits=self.n_rabbit,
            width=self.grid.width,
            height=self.grid.height,
            algorithm=str(algorithm),
        )
        self.done = False

    def reset(self):
        self.done = False
        self.snake.body = [(10, 10), (10, 11), (10, 12)]
        self.rabbits.clear()
        self.rabbits.extend(
            create_rabbits(self.grid.width, self.grid.height, self.n_rabbit))
        self.directions.clear()
        self.performance_tracker = PerformanceTracker(
            n_rabbits=self.n_rabbit,
            width=self.grid.width,
            height=self.grid.height,
            algorithm=str(self.algorithm),
        )

    def update(self):
        pass
        self.grid.update(snake=self.snake, rabbits=self.rabbits)
        if not self.directions:
            if not self.rabbits:
                self.win()
            else:
                if str(self.algorithm) == "ActorCriticAlgorithm":
                    state = self.get_state()
                self.directions = self.algorithm.define_new_directions(
                    rabbits=self.rabbits, snake=self.snake, grid=self.grid)
                if not self.directions:
                    print(
                        "Warning: No valid directions returned by the algorithm. "
                    )
                    self.loose()
                    return
        self.move_snake()
        reward = 1 if self.check_eat() else 0
        reward = -1 if self.check_collision() else reward
        if self.algorithm == "ActorCritic":
            next_state = self.get_state()
            return self.algorithm.train_step(
                state=state,
                action=self.snake.direction,
                reward=reward,
                next_state=next_state,
                done=self.done,
            )

    def check_collision(self):
        x_head, y_head = self.snake.get_head()
        head = self.snake.get_head()

        if not (0 <= x_head < self.grid.width
                and 0 <= y_head < self.grid.height):
            print(f"Snake out of bounds: head position ({x_head}, {y_head})")
            self.loose()
            return True

        elif head in self.snake.body[1:]:
            print(f"Snake collision with itself at {head}")
            self.loose()
            return True
        return False

    # def define_new_directions(self):
    #     state = self.get_state()
    #     action = self.training_handler.select_action(intial_state=state)
    #     self.directions = [action]

    def check_eat(self):
        head = self.snake.get_head()
        x_head, y_head = head[0], head[1]
        for rabbit_ in self.rabbits:
            if rabbit_.x == x_head and rabbit_.y == y_head:
                self.performance_tracker.increment_lapins_manges()
                self.rabbits.remove(rabbit_)
                self.snake.grow()
                print(f"Rabbit eaten at ({x_head}, {y_head})")
                return True
        return False

    def move_snake(self):
        if self.directions:
            new_direction = self.directions.pop(0)
            self.snake.change_direction(new_direction)
        else:
            print("No directions available, snake is not moving.")
        self.snake.move()
        self.performance_tracker.increment_movements()

    def win(self):
        self.done = True
        self.performance_tracker.win = True
        self.performance_tracker.save_performance()
        self.game_won.emit()

    def loose(self):
        self.done = True
        self.performance_tracker.save_performance()
        self.game_lost.emit()

    def stop(self):
        self.game_stop.emit()

    def get_state(self):
        state = [
            self.grid.width, self.grid.height,
            self.algorithm.REVERSE_ACTION_MAP[self.snake.direction]
        ]
        for bodypart in self.snake.body:
            state.append(bodypart[0])
            state.append(bodypart[1])
        for rabbit_ in self.rabbits:
            state.append(rabbit_.x)
            state.append(rabbit_.y)
        return np.array(state)
