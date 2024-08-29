import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Suivi des touches du clavier')
        self.resize(400, 300)
        self.setFocus()

    def keyPressEvent(self, event):
        key = event.key()
        print(f'Touche pressée : {key}')
        if key == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
