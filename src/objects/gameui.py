from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

from src.objects.grid import Grid
from src.utils.constants import height, width, nb_lapins

nb_lapins = nb_lapins()


class GameWindow(QWidget):

    def __init__(self, grid: Grid):
        super(GameWindow, self).__init__()
        self.init_ui(grid=grid)

    def init_ui(self, grid):
        layout = QHBoxLayout()
        self.menu = MenuUI()
        layout.addWidget(self.menu)

        self.game_interface = GameInterface(grid)
        layout.addWidget(self.game_interface)
        self.setLayout(layout)


class MenuUI(QWidget):
    game_started = pyqtSignal()

    def __init__(self):
        super(MenuUI, self).__init__()
        # Menu-specific elements
        layout = QVBoxLayout()

        algorithm_label = QLabel("Algorithm")
        combo = QComboBox()
        combo.addItems(["A-étoile"])

        start_button = QPushButton("Start Game")
        start_button.clicked.connect(self.start_game)

        layout.addWidget(algorithm_label)
        layout.addWidget(combo)
        layout.addWidget(start_button)

        self.setLayout(layout)

    def start_game(self):
        # Update state (example)
        self.current_state = "game"
        # Emit a signal to trigger the game interface
        self.game_started.emit()


class GameInterface(QWidget):

    def __init__(self, grid):
        super(GameInterface, self).__init__()
        self.grid = grid

    def paintEvent(self, event):
        painter = QPainter(self)
        self.grid.draw(painter)
