import random

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QMainWindow, QWidget

from objects import rabbit
from objects.grid import Grid
from objects.rabbit import Rabbit
from objects.snake import Snake
from objects.utils import height, width

nb_lapins = 10


class GameBoard(QMainWindow):

    def __init__(self):
        super().__init__()
        self.snake = Snake()
        self.rabbits = [
            Rabbit(random.randrange(width()), random.randrange(height()))
            for _ in range(nb_lapins)
        ]
        self.grid = Grid()

        self.setWindowTitle("Jeu Snake")
        self.setGeometry(0, 0, width() * 10, height() * 10)
        self.setFocus()
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(100)

        self.show()

    def keyPressEvent(self, event):
        key = event.key()
        self.snake.change_direction(key)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.grid.draw(painter)

    def timerEvent(self):
        self.snake.move()
        self.check_collision()
        self.check_eat()
        self.grid.update(snake=self.snake, rabbits=self.rabbits)
        self.update()

    def check_collision(self):
        head = self.snake.body[0]
        x_head, y_head = head[0], head[1]

        if not (0 <= x_head < width()
                and 0 <= y_head < height()) or (head in self.snake.body[1:]):
            self.timer.stop()
            self.close()
            print("Collision")

    def check_eat(self):
        head = self.snake.body[0]
        x_head, y_head = head[0], head[1]
        for rabbit in self.rabbits:
            if rabbit.x == x_head and rabbit.y == y_head:
                self.rabbits.remove(rabbit)
                self.snake.grow()
