import random

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QMainWindow

from src.objects.grid import Grid
from src.objects.rabbit import Rabbit
from src.objects.snake import Snake
from src.utils.astar import shortest_path
from src.utils.constants import height, width, nb_lapins
from src.utils.utils import choose_direction

nb_lapins = nb_lapins()


class GameBoard(QMainWindow):

    def __init__(self):
        super().__init__()
        self.snake = Snake()
        self.rabbits = [
            Rabbit(random.randrange(width()), random.randrange(height()))
            for _ in range(nb_lapins)
        ]
        self.grid = Grid()
        self.directions = []
        self.setWindowTitle("Jeu Snake")
        self.setGeometry(0, 0, width() * 10, height() * 10)
        self.setFocus()
        self.grid.update(snake=self.snake, rabbits=self.rabbits)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(150)

        self.show()

    # def keyPressEvent(self, event):
    #     key = event.key()
    #     self.snake.change_direction(key)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.grid.draw(painter)

    def timerEvent(self):

        snake_head = self.snake.get_head()
        snake_head_node = self.grid.get_node(snake_head[0], snake_head[1])
        if not self.directions:
            self.define_new_directions(snake_head_node)
        if self.directions:
            new_direction = self.directions.pop(0)
            self.snake.change_direction(new_direction)
        self.snake.move()
        self.check_collision()
        self.check_eat()
        self.grid.update(snake=self.snake, rabbits=self.rabbits)
        self.update()

    def define_new_directions(self, snake_head_node):
        if not self.rabbits:
            self.win()
        next_rabbit = self.closest_rabbit()
        rabbit_node = self.grid.get_node(next_rabbit.pos())
        next_nodes = shortest_path(self.grid,
                                   start=snake_head_node,
                                   end=rabbit_node)

        if not next_nodes:
            self.timer.stop()
            self.close()
            print("Loose !")
            return
        self.directions = [
            choose_direction(n1=next_nodes[i], n2=next_nodes[i + 1])
            for i in range(len(next_nodes) - 1)
        ]

    def check_collision(self):
        head = self.snake.get_head()
        x_head, y_head = head[0], head[1]
        if not (0 <= x_head < width()
                and 0 <= y_head < height()) or (head in self.snake.body[1:]):
            self.stop()
            print("Collision")

    def check_eat(self):
        head = self.snake.get_head()
        x_head, y_head = head[0], head[1]
        for rabbit_ in self.rabbits:
            if rabbit_.x == x_head and rabbit_.y == y_head:

                self.rabbits.remove(rabbit_)
                self.snake.grow()

    def closest_rabbit(self):
        head = self.snake.get_head()
        head_node = self.grid.get_node(head)
        next_rabbit = min(self.rabbits,
                          key=lambda p: (p.x - head_node.x)**2 +
                          (p.y - head_node.y)**2)
        return next_rabbit

    def win(self):
        self.stop()
        print("Win !")

    def stop(self):
        self.timer.stop()
        self.close()

    def loose(self):
        self.stop()
        print("Loose !")
