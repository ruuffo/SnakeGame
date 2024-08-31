from PyQt5.QtCore import Qt

choose_direction = lambda n1, n2: (Qt.Key_Right
                                   if n2.x - n1.x > 0 else Qt.Key_Left
                                   if n2.x - n1.x < 0 else Qt.Key_Down
                                   if n2.y - n1.y > 0 else Qt.Key_Up)
