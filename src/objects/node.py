from src.utils.constants import empty_cell_grid_code


class Node:

    def __init__(
        self,
        x: int,
        y: int,
        walkable: bool = True,
        kind: int = empty_cell_grid_code(),
        **kwargs
    ):
        self.x = x
        self.y = y
        self.heuristic = 0
        self.cost = 0
        self.parent = kwargs.get("parent", None)
        self.walkable = walkable
        self.kind = kind

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self) -> str:
        return self.pos()

    def pos(self) -> tuple:
        return self.x, self.y
