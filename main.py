import sys

from PyQt5.QtWidgets import QApplication

from src.objects.gameboard import GameBoard

HEIGHT = 48
WIDTH = 75

if __name__ == '__main__':
    app = QApplication(sys.argv)
    snake_game = GameBoard()
    sys.exit(app.exec_())
