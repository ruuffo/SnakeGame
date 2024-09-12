from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
from src.objects.actorcritic import ActorCritic
from src.objects.actorcriticalgorithm import ActorCriticAlgorithm
from src.objects.gameengine import GameEngine
from src.objects.gameui import GameWindow
from src.objects.grid import Grid
from src.objects.snake import Snake
from src.utils.astar import Astar
from src.utils.utils import create_rabbits


class SnakeGame(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.snake = None
        self.rabbits = []
        self.grid = None

        self.game_window = GameWindow(None)
        self.game_window.menu.game_start_signal.connect(self.on_game_start)
        self.game_window.menu.game_stop_signal.connect(self.on_game_stop)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)

        self.game_window.show()

    def on_game_start(self):
        self.on_game_stop()
        width, height, nb_rabbits, one_rabbit_mode = (
            self.game_window.menu.current_width,
            self.game_window.menu.current_height,
            self.game_window.menu.current_n_rabbits,
            self.game_window.menu.one_rabbit_mode)

        self.snake = Snake()
        self.grid = Grid(width=width, height=height)
        self.game_window.game_interface.grid = self.grid

        algorithm_text = self.game_window.menu.algorithm_combobox.currentText()
        algorithm = None
        if algorithm_text == "A-étoile":
            algorithm = Astar()
        elif algorithm_text == "Actor-Critic":
            algorithm = ActorCriticAlgorithm(ActorCritic(4))

        self.rabbits.clear()
        self.rabbits.extend(
            create_rabbits(width=width,
                           height=height,
                           n_rabbits=nb_rabbits,
                           snake=self.snake))

        self.engine = GameEngine(snake=self.snake,
                                 rabbits=self.rabbits,
                                 grid=self.grid,
                                 algorithm=algorithm,
                                 one_rabbit_mode=one_rabbit_mode)
        self.engine.game_won.connect(self.on_game_won)
        self.engine.game_lost.connect(self.on_game_lost)
        self.engine.game_stop.connect(self.on_game_stop)
        print("Game start")
        self.timer.start(100)

    def timerEvent(self):
        if self.engine:
            self.engine.update()
            self.game_window.update()

    def on_game_won(self):
        print("Vous avez gagné!")
        self.restart_or_not()

    def on_game_lost(self):
        print("Vous avez perdu!")
        self.restart_or_not()

    def on_game_stop(self):
        self.timer.stop()

    def restart_or_not(self):
        self.on_game_stop()
        if self.game_window.menu.infinite_loop:
            self.engine.reset()
            self.timer.start(100)
