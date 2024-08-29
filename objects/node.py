from objects.utils import empty_cell_grid_code


class Node:

    def __init__(self, x: int, y: int, walkable: bool = True, kind: int = empty_cell_grid_code):
        self.x = x
        self.y = y
        self.h = 0
        self.walkable = walkable
        self.g = float("inf")
        self.f = float("inf")
        self.kind = kind
