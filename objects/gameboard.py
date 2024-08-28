from PyQt5.QtCore import QRectF, QTimer, Qt
from PyQt5.QtGui import QBrush, QPaintEvent, QPainter
from PyQt5.QtWidgets import QWidget

from objects.grid import Grid
from objects.snake import Snake


class GameBoard(QWidget):

    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.snake = Snake()
        self.grid = Grid()

        self.setWindowTitle("Jeu Snake")
        self.setGeometry(100, 100, width * 10, height * 10)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(100)

        self.show()

    def keyPressEvent(self, event):
        self.snake.change_direction(event.key())

    def paintEvent(self, event):
        painter = QPainter(self)
        self.grid.draw(painter)

    def timerEvent(self): 
        self.snake.move()
        self.check_collision()
        # self.paintEvent(None)
        self.update()

    def check_collision(self):
        head = self.snake.body[0]
        x_head, y_head = head[0], head[1]
        if not (0 <= x_head < self.width
                or 0 <= y_head < self.height) or head in self.snake.body[1:]:
            self.timer.stop()
            print("stop")
