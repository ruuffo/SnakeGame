from objects.node import Node


class Grid:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.nodes = [[Node(x, y) for y in range(height)]
                      for x in range(width)]

    def get_node(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.nodes[x][y]
        else:
            return None

    def get_neighbors(self, node):
        x, y = node.x, node.y
        return [
            self.get_node(x - 1, y),
            self.get_node(x + 1, y),
            self.get_node(x, y + 1),
            self.get_node(x, y - 1)
        ]
    def draw(self):
        for x in range(len(self.nodes)):
            for y in range(len(self.nodes[0])):
                node = self.nodes[x][y]
                if node.kind == :
