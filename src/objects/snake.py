from __future__ import annotations
from PyQt5.QtCore import Qt

from src.utils.utils import convert_direction_to_qt_keymap


class Snake:
    GRID_CODE = 2

    def __init__(
        self,
        direction=Qt.Key_Down,
        body=None,
    ):
        self.direction = direction
        if body is None:
            self.body = [(10, 10), (11, 10),
                         (12, 10)]  # Default starting position
        else:
            self.body = body

    def change_direction(self, direction):
        if not ((self.direction == Qt.Key_Down and direction == Qt.Key_Up) or
                (self.direction == Qt.Key_Up and direction == Qt.Key_Down) or
                (self.direction == Qt.Key_Left and direction == Qt.Key_Right)
                or
                (self.direction == Qt.Key_Right and direction == Qt.Key_Left)):
            self.direction = direction

    def possible_moves(self, grid: "Grid"):
        head = self.get_head()
        head_node = grid.get_node(head)
        neighbors = [
            neighbor for neighbor in grid.get_neighbors(head_node)
            if neighbor.walkable
        ]
        possible_moves = [
            convert_direction_to_qt_keymap(head_node, neighbor)
            for neighbor in neighbors
        ]
        return possible_moves

    def move(self):

        head = self.body[0]
        x, y = head[0], head[1]

        if self.direction == Qt.Key_Left:
            x -= 1
        elif self.direction == Qt.Key_Right:
            x += 1
        elif self.direction == Qt.Key_Down:
            y += 1
        elif self.direction == Qt.Key_Up:
            y -= 1
        new_head = x, y
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        self.body = self.body + [self.body[-1]]

    def get_head(self):
        return self.body[0]
