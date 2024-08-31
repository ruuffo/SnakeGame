import heapq
from src.objects.grid import Grid
from src.objects.node import Node


def compare_heuristic(node1: Node, node2: Node) -> int:
    if node1.heuristic < node2.heuristic:
        return 1
    elif node1.heuristic == node2.heuristic:
        return 0
    else:
        return -1


def shortest_path(grid: Grid, start: Node, end: Node):
    closed_list = []
    open_list = []
    heapq.heappush(open_list, start)

    while True:
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)
        if current_node == end:
            return definePath(current_node)

        neighbors = grid.get_neighbors(current_node)

        for neighbor in neighbors:
            if not neighbor.walkable:
                continue
            next = Node(neighbor.x, neighbor.y, parent=current_node)
            if next in closed_list:
                continue
            next.cost = current_node.cost + 1
            next.heuristic = manhattan_distance(neighbor, end)
            next.f = next.cost + next.heuristic
            if all(next.f < node.f for node in open_list if next == node):
                heapq.heappush(open_list, next)
        if not open_list:
            return None


def definePath(node: Node) -> list:
    path = []
    while node:
        path.append(node)
        node = node.parent
    return path[::-1]


def manhattan_distance(n1: Node, n2: Node) -> int:
    """retourne la distance de manhattan entre deux noeuds

    Args:
        n1 (Node): noeud 1
        n2 (Node): noeud 2

    Returns:
        int: distance
    """
    return abs(n1.x - n2.x) + abs(n1.y - n2.y)
