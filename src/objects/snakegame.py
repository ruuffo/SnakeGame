import random
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
from src.objects.gameengine import GameEngine
from src.objects.gameui import GameWindow
from src.objects.grid import Grid
from src.objects.snake import Snake
from src.utils.astar import Astar
from src.utils.utils import create_rabbits


class SnakeGame(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.snake = Snake()
        self.rabbits = []
        self.grid = None

        self.game_window = GameWindow(self.grid)
        self.game_window.menu.game_started.connect(self.on_game_start)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)

        self.game_window.show()

    def on_game_start(self):
        width, height, nb_rabbits = (
            self.game_window.menu.current_width,
            self.game_window.menu.current_height,
            self.game_window.menu.current_n_rabbits,
        )
        self.grid = Grid(width=width, height=height)
        self.game_window.game_interface.grid = self.grid

        algorithm_text = self.game_window.menu.combo.currentText()
        if algorithm_text == "A-étoile":
            algorithm = Astar()

        self.rabbits.clear()
        self.rabbits.extend(create_rabbits(width, height, nb_lapins=nb_rabbits))

        self.engine = GameEngine(
            snake=self.snake, rabbits=self.rabbits, grid=self.grid, algorithm=algorithm
        )
        self.engine.game_won.connect(self.on_game_won)
        self.engine.game_lost.connect(self.on_game_lost)
        self.engine.game_stop.connect(self.on_game_stop)

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
