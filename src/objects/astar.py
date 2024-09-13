import heapq
from typing import List

from PyQt5.QtCore import Qt
from src.objects.pathfindingalgorithm import PathfindingAlgorithm
from src.objects.rabbit import Rabbit
from src.objects.snake import Snake
from src.objects.grid import Grid
from src.objects.node import Node
from src.utils.utils import convert_direction_to_qt_keymap


class Astar(PathfindingAlgorithm):

    def shortest_path(self, grid: Grid, start: Node, end: Node):
        closed_list = []
        open_list = []
        heapq.heappush(open_list, start)

        while True:
            current_node = heapq.heappop(open_list)
            closed_list.append(current_node)
            if current_node == end:
                return self.definePath(current_node)

            neighbors = grid.get_neighbors(current_node)

            for neighbor in neighbors:
                if not neighbor.walkable:
                    continue
                next = Node(neighbor.x, neighbor.y, parent=current_node)
                if next in closed_list:
                    continue
                next.cost = current_node.cost + 1
                next.heuristic = self.manhattan_distance(neighbor, end)
                next.f = next.cost + next.heuristic
                if all(next.f < node.f for node in open_list if next == node):
                    heapq.heappush(open_list, next)
            if not open_list:
                return None

    def compute(self, grid: Grid, snake: Snake,
                rabbits: List[Rabbit]) -> List[Qt.Key]:

        head = snake.get_head()
        head_node = grid.get_node(head)

        next_rabbit = self.closest_rabbit(snake=snake,
                                          rabbits=rabbits,
                                          grid=grid)
        rabbit_node = grid.get_node(next_rabbit.pos())

        next_nodes = self.shortest_path(grid, start=head_node, end=rabbit_node)

        if next_nodes is None:
            return None

        directions = [
            convert_direction_to_qt_keymap(start_node=next_nodes[i],
                                           end_node=next_nodes[i + 1])
            for i in range(len(next_nodes) - 1)
        ]
        return directions

    def definePath(self, node: Node) -> list:
        path = []
        while node:
            path.append(node)
            node = node.parent
        return path[::-1]

    def manhattan_distance(self, n1: Node, n2: Node) -> int:
        """retourne la distance de manhattan entre deux noeuds

        Args:
            n1 (Node): noeud 1
            n2 (Node): noeud 2

        Returns:
            int: distance
        """
        return abs(n1.x - n2.x) + abs(n1.y - n2.y)

    def closest_rabbit(self, snake: Snake, grid: Grid, rabbits: List[Rabbit]):
        head = snake.get_head()
        head_node = grid.get_node(head)

        next_rabbit = min(
            rabbits,
            key=lambda p: (p.x - head_node.x)**2 + (p.y - head_node.y)**2,
        )

        return next_rabbit
