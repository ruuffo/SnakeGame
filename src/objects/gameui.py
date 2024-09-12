from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.objects.grid import Grid


class GameWindow(QWidget):

    def __init__(self, grid: Grid):
        super(GameWindow, self).__init__()
        self.grid = grid
        self.game_interface = None
        self.init_ui()

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.menu = MenuUI()
        self.menu.game_start_signal.connect(self.start_game)
        self.layout.addWidget(self.menu)

        self.setLayout(self.layout)
        self.show()

    def start_game(self):
        # Remove the menu from the layout (optional, if you want the game to replace the menu)
        if self.game_interface is not None:
            self.layout.removeWidget(self.game_interface)
            self.game_interface.deleteLater()  # Remove the previous game interface if it exists
        width, height = self.menu.current_width * 10, self.menu.current_height * 10
        # Create the game interface and add it to the layout
        self.game_interface = GameInterface(self.grid, width=width, height=height)
        self.layout.addWidget(self.game_interface)

        # Refresh the layout to show the game interface
        self.update()


class MenuUI(QWidget):
    game_start_signal = pyqtSignal()
    game_stop_signal = pyqtSignal()

    def __init__(self):
        super(MenuUI, self).__init__()
        # Menu-specific elements
        layout = QVBoxLayout()

        algorithm_label = QLabel("Algorithm")
        self.algorithm_combobox = QComboBox()
        self.algorithm_combobox.addItems(["A-étoile", "Actor-Critic"])

        self.current_width, self.current_height = 20, 20

        self.width_label = QLabel(f"Width: {self.current_width}")
        self.width_slider = QSlider(orientation=Qt.Horizontal)
        self.width_slider.setRange(20, 150)
        self.width_slider.blockSignals(True)
        self.width_slider.setValue(self.current_width)
        self.width_slider.blockSignals(False)
        self.width_slider.valueChanged.connect(self.update_slider_width)

        self.height_label = QLabel(f"Height: {self.current_height}")
        self.height_slider = QSlider(orientation=Qt.Horizontal)
        self.height_slider.setRange(20, 100)
        self.height_slider.blockSignals(True)
        self.height_slider.setValue(self.current_width)
        self.height_slider.blockSignals(False)
        self.height_slider.valueChanged.connect(self.update_slider_height)


        self.current_n_rabbits = 1
        self.rabbits_label = QLabel(f"number of rabbits: {self.current_n_rabbits}")
        self.rabbits_spinbox = QSpinBox()
        self.rabbits_spinbox.valueChanged.connect(self.update_n_rabbits)
        self.rabbits_spinbox.setMinimum(1)

        self.thresh = 80
        self.rabbits_spinbox.setMaximum(self.thresh)

        self.infinite_loop = True
        infinite_loop_label = QLabel("Infinite loop")
        self.infinite_loop_checkbox = QCheckBox()
        self.infinite_loop_checkbox.setCheckState(Qt.Checked)
        self.infinite_loop_checkbox.stateChanged.connect(
            self.infinite_loop_change_state
        )

        self.one_rabbit_mode = False
        self.one_rabbit_mode_label = QLabel("One Rabbit Mode")
        self.one_rabbit_mode_checkbox = QCheckBox()
        self.one_rabbit_mode_checkbox.setCheckState(Qt.Unchecked)
        self.one_rabbit_mode_checkbox.stateChanged.connect(self.one_rabbit_mode_checkbox_change_state)


        button_layout = QHBoxLayout()
        start_button = QPushButton("Start")
        stop_button = QPushButton("Stop")

        start_button.clicked.connect(self.start_game)
        stop_button.clicked.connect(self.stop_game)

        button_layout.addWidget(start_button)
        button_layout.addWidget(stop_button)

        layout.addWidget(self.width_label)
        layout.addWidget(self.width_slider)
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_slider)
        layout.addWidget(self.rabbits_spinbox)

        layout.addWidget(algorithm_label)
        layout.addWidget(self.algorithm_combobox)
        layout.addWidget(infinite_loop_label)
        layout.addWidget(self.infinite_loop_checkbox)
        layout.addWidget(self.one_rabbit_mode_label)
        layout.addWidget(self.one_rabbit_mode_checkbox)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_slider_width(
        self,
    ):
        self.current_width = self.width_slider.value()
        self.thresh = self.compute_thresh()
        self.rabbits_spinbox.setMaximum(self.thresh)
        self.width_label.setText(f"Width: {self.current_width}")

    def update_slider_height(
        self,
    ):
        self.current_height = self.height_slider.value()
        self.thresh = self.compute_thresh()
        self.rabbits_spinbox.setMaximum(self.thresh)
        self.height_label.setText(f"Height: {self.current_height}")

    def compute_thresh(self):
        return int(self.current_width * self.current_height * 0.3)

    def start_game(self):
        # Emit the signal to trigger the game interface
        self.game_start_signal.emit()

    def stop_game(self):
        self.game_stop_signal.emit()

    def update_n_rabbits(self):
        self.current_n_rabbits = self.rabbits_spinbox.value()

    def infinite_loop_change_state(self):
        self.infinite_loop = self.infinite_loop_checkbox.isChecked()
    def one_rabbit_mode_checkbox_change_state(self):
        self.one_rabbit_mode = self.one_rabbit_mode_checkbox.isChecked()
        if self.one_rabbit_mode:
            self.rabbits_spinbox.setValue(1)
            self.rabbits_spinbox.setEnabled(False)
        else:
            self.rabbits_spinbox.setEnabled(True)



class GameInterface(QWidget):

    def __init__(self, grid, height, width):
        super(GameInterface, self).__init__()
        self.grid = grid
        self.setFixedSize(width, height)

    def paintEvent(self, event):

        self.resize(self.grid.width * 10, self.grid.height * 10)
        painter = QPainter(self)
        self.grid.draw(painter)
