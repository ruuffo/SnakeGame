
from PyQt5.QtCore import QObject, pyqtSignal
from src.utils.astar import shortest_path
from src.utils.constants import height, width
from src.utils.utils import choose_direction


class GameEngine(QObject):
    game_won = pyqtSignal()
    game_lost = pyqtSignal()

    def __init__(self, snake, rabbits, grid):
        super().__init__()
        self.snake = snake
        self.rabbits = rabbits
        self.grid = grid
        self.directions = []

    def update(self):
        if not self.directions:
            self.define_new_directions()
        self.move_snake()
        self.check_collision()
        self.check_eat()
        self.grid.update(snake=self.snake, rabbits=self.rabbits)

    def check_collision(self):
        head = self.snake.get_head()
        x_head, y_head = head[0], head[1]
        if not (0 <= x_head < width()
                and 0 <= y_head < height()) or (head in self.snake.body[1:]):
            self.loose()
            print("Collision")


    def define_new_directions(self):
        if not self.rabbits:
            self.win()
            return

        head = self.snake.get_head()
        head_node = self.grid.get_node(head)

        next_rabbit = self.closest_rabbit()
        rabbit_node = self.grid.get_node(next_rabbit.pos())

        next_nodes = shortest_path(self.grid,
                                   start=head_node,
                                   end=rabbit_node)

        if not next_nodes:
            self.loose()
            return

        self.directions = [
            choose_direction(n1=next_nodes[i], n2=next_nodes[i + 1])
            for i in range(len(next_nodes) - 1)
        ]

    def check_eat(self):
        head = self.snake.get_head()
        x_head, y_head = head[0], head[1]
        for rabbit_ in self.rabbits:
            if rabbit_.x == x_head and rabbit_.y == y_head:

                self.rabbits.remove(rabbit_)
                self.snake.grow()

    def move_snake(self):
        if self.directions:
            new_direction = self.directions.pop(0)
            self.snake.change_direction(new_direction)
        self.snake.move()

    def closest_rabbit(self):
        head = self.snake.get_head()
        head_node = self.grid.get_node(head)

        next_rabbit = min(self.rabbits,
                          key=lambda p: (p.x - head_node.x)**2 +
                          (p.y - head_node.y)**2)
        return next_rabbit

    def win(self):
        self.game_won.emit()

    def loose(self):
        self.game_lost.emit()
