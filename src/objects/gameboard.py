import random
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
from src.objects.pathfindingalgorithm import PathfindingAlgorithm
from src.objects.gameengine import GameEngine
from src.objects.gameui import GameInterface, GameWindow, MenuUI
from src.objects.grid import Grid
from src.objects.rabbit import Rabbit
from src.objects.snake import Snake
from src.utils.constants import height, nb_lapins, width
from src.utils.astar import Astar
from src.utils.utils import create_rabbits


class GameBoard(QWidget):

    def __init__(self, algorithm: PathfindingAlgorithm = Astar()) -> None:
        super().__init__()
        self.snake = Snake()

        self.rabbits = create_rabbits(width=width(),
                                      height=height(),
                                      nb_lapins=nb_lapins())

        self.grid = Grid()

        self.engine = GameEngine(self.snake,
                                 self.rabbits,
                                 self.grid,
                                 algorithm=algorithm)

        self.engine.game_won.connect(self.on_game_won)
        self.engine.game_lost.connect(self.on_game_lost)
        self.engine.game_stop.connect(self.on_game_stop)
        self.game_window = GameWindow(self.grid)
        self.game_window.menu.game_started.connect(self.on_game_start)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)

        self.game_window.show()

    def on_game_start(self):
        self.timer.start(100)

    def timerEvent(self):
        self.engine.update()
        self.game_window.update()

    def on_game_won(self):
        print("Vous avez gagné!")

    def on_game_lost(self):
        print("Vous avez perdu!")

    def on_game_stop(self):
        self.timer.stop()
        time.sleep(3)
        self.ui.close()
