from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QMainWindow

from src.utils.constants import height, width, nb_lapins


nb_lapins = nb_lapins()


class GameUI(QMainWindow):

    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.setWindowTitle("Jeu Snake")
        self.setGeometry(0, 0, width() * 10, height() * 10)
        self.setFocus()
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.grid.draw(painter)
