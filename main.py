import sys
from PyQt5.QtWidgets import QApplication

from src.objects.gameboard import GameBoard

if __name__ == '__main__':
    app = QApplication(sys.argv)
    snake_game = GameBoard()
    sys.exit(app.exec_())
