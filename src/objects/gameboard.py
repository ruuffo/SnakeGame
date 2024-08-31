import random

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QMainWindow

from src.objects import rabbit
from src.objects.grid import Grid
from src.objects.rabbit import Rabbit
from src.objects.snake import Snake
from src.utils.astar import shortest_path
from src.utils.constants import height, width
from src.utils.utils import compute_direction

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
        self.movements = []
        self.setWindowTitle("Jeu Snake")
        self.setGeometry(0, 0, width() * 10, height() * 10)
        self.setFocus()
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(100)

        self.show()

    # def keyPressEvent(self, event):
    #     key = event.key()
    #     self.snake.change_direction(key)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.grid.draw(painter)

    def timerEvent(self):
        snake_head = self.snake.body[0]
        snake_head_node = self.grid.get_node(snake_head[0], snake_head[1])
        if not self.movements:

            random_rabbit = random.choice(self.rabbits)
            # self.rabbits.remove(random_rabbit)
            rabbit_node = self.grid.get_node(random_rabbit.x, random_rabbit.y)
            self.movements = shortest_path(self.grid,
                                           start=snake_head_node,
                                           end=rabbit_node)
        next_node = self.movements.pop(0)
        new_direction = compute_direction(next_node=next_node,
                                          current_node=snake_head_node)
        self.snake.change_direction(new_direction)
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
        for rabbit_ in self.rabbits:
            if rabbit_.x == x_head and rabbit_.y == y_head:
                pass
                self.rabbits.remove(rabbit_)
                self.snake.grow()
                break
