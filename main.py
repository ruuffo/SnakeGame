import sys
from PyQt5.QtWidgets import QApplication

from src.objects.snakegame import SnakeGame

if __name__ == '__main__':
    app = QApplication(sys.argv)
    snake_game = SnakeGame()
    sys.exit(app.exec_())
