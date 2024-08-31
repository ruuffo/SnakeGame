from PyQt5.QtCore import Qt


def choose_direction(n1, n2):
    if n2.x - n1.x > 0:
        return Qt.Key_Right
    elif n2.x - n1.x < 0:
        return Qt.Key_Left
    elif n2.y - n1.y > 0:
        return Qt.Key_Down
    else:
        return Qt.Key_Up
