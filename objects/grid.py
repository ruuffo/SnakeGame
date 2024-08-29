from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor

from objects.node import Node
from objects.rabbit import Rabbit
from objects.snake import Snake
from objects.utils import empty_cell_grid_code, height, width


class Grid:
    """Objet Grille, qui permet d'avoir la logique du graphe.
    """

    def __init__(self):
        self.nodes = [[Node(x, y) for y in range(height())]
                      for x in range(width())]

    def get_node(self, x, y):
        if 0 <= x < width() and 0 <= y < height():
            return self.nodes[x][y]
        else:
            return None

    def get_neighbors(self, node):
        x, y = node.x, node.y
        return [
            self.get_node(x - 1, y),
            self.get_node(x + 1, y),
            self.get_node(x, y + 1),
            self.get_node(x, y - 1)
        ]

    def draw(self, painter):
        for x in range(len(self.nodes)):
            for y in range(len(self.nodes[0])):
                painter.setPen(QColor(0, 0, 0, 0))
                painter.setBrush(QBrush(Qt.white))
                node = self.nodes[x][y]
                if node.kind == Snake.GRID_CODE:
                    painter.setBrush(QBrush(Qt.green))
                elif node.kind == Rabbit.GRID_CODE:
                    painter.setBrush(QBrush(Qt.red))

                painter.drawRect(x * 10, y * 10, 10, 10)

    def update(self, snake, rabbits):
        for x in range(len(self.nodes)):
            for y in range(len(self.nodes[0])):
                self.nodes[x][y].kind = empty_cell_grid_code()
        for bodypart in snake.body:
            x, y = bodypart[0], bodypart[1]
            if self.get_node(x, y) is not None:
                self.nodes[x][y].kind = Snake.GRID_CODE

        for rabbit in rabbits:
            self.nodes[rabbit.x][rabbit.y].kind = Rabbit.GRID_CODE
