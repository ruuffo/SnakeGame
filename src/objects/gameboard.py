import random
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
from src.objects.gameengine import GameEngine
from src.objects.gameui import GameUI
from src.objects.grid import Grid
from src.objects.rabbit import Rabbit
from src.objects.snake import Snake
from src.utils.constants import height, nb_lapins, width


class GameBoard(QWidget):

    def __init__(self, ) -> None:
        super().__init__()
        self.snake = Snake()
        self.rabbits = [
            Rabbit(random.randrange(width()), random.randrange(height()))
            for _ in range(nb_lapins())
        ]
        self.grid = Grid()
        self.engine = GameEngine(self.snake, self.rabbits, self.grid)

        self.engine.game_won.connect(self.on_game_won)
        self.engine.game_lost.connect(self.on_game_lost)


        self.ui = GameUI(self.grid)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(100)

        self.ui.show()

    def timerEvent(self):
        self.engine.update()
        self.ui.update()

    def on_game_won(self):
        self.timer.stop()
        print("Vous avez gagné!")
        time.sleep(3)
        self.ui.close()

    def on_game_lost(self):
        self.timer.stop()
        print("Vous avez perdu!")
        time.sleep(3)
        self.ui.close()
