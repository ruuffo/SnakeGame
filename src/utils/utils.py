from PyQt5.QtCore import Qt
from src.objects.node import Node


def compute_direction(next_node: Node, current_node: Node):
    dx, dy = current_node.x - next_node.x, current_node.y - next_node.y
    if dx < 0:
        return Qt.Key_Right
    elif dx > 0:
        return Qt.Key_Left
    elif dy < 0:
        return Qt.Key_Up
    else:
        return Qt.Key_Down
