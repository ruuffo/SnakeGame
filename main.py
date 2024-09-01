import sys

from PyQt5.QtWidgets import QApplication

from src.objects.gameboard import GameBoard
from src.objects.gameui import GameUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    snake_game = GameBoard()
    sys.exit(app.exec_())
