import sys
from PyQt5.QtWidgets import QApplication

from objects.gameboard import GameBoard

HEIGHT = 48
WIDTH = 75


def heuristic(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)


def jump(grid, node, parent, end):
    """
    Effectue un saut de point à point pour trouver un "jump point" dans une direction donnée.

    Args:
        grid (Grid): La grille contenant les nœuds.
        node (Node): Le nœud courant à examiner.
        parent (Node): Le nœud parent d'où provient le saut.
        end (Node): Le nœud cible à atteindre.

    Returns:
        Node: Le point de saut (jump point) trouvé, ou None s'il n'y a pas de point pertinent.
    """
    if not node.walkable:
        return None

    x, y = node.x, node.y
    px, py = parent.x, parent.y

    dx, dy = x - px, y - py

    if node == end:
        return node

    # Pour les mouvements horizontaux ou verticaux, on vérifie les voisins orthogonaux
    if dx != 0:
        if (grid.get_node(x + dx, y + 1)
                and not grid.get_node(x, y + 1).walkable
                and grid.get_node(x + dx, y + 1).walkable) or (
                    grid.get_node(x + dx, y - 1)
                    and not grid.get_node(x, y - 1).walkable
                    and grid.get_node(x + dx, y - 1).walkable):
            return node
    elif dy != 0:
        if (grid.get_node(x + 1, y + dy)
                and not grid.get_node(x + 1, y).walkable
                and grid.get_node(x + 1, y + dy).walkable) or (
                    grid.get_node(x - 1, y + dy)
                    and not grid.get_node(x - 1, y).walkable
                    and grid.get_node(x - 1, y + dy).walkable):
            return node

    # Recursion pour continuer à sauter dans la direction actuelle
    if dx != 0 and dy != 0:
        if jump(grid=grid, node=grid.get_node(x + dx, y), parent=node,
                end=end) or jump(grid=grid,
                                 node=grid.get_node(x, y + dy),
                                 parent=node,
                                 end=end):
            return node
    elif dx != 0:
        return jump(grid, grid.get_node(x + dx, y), node, end)
    elif dy != 0:
        return jump(grid, grid.get_node(x, y + dy), node, end)

    return None


def jps(grid, start, end):
    """
    Implémente l'algorithme Jump Point Search pour trouver le chemin le plus court.

    Args:
        grid (Grid): La grille contenant les nœuds.
        start (Node): Le nœud de départ.
        end (Node): Le nœud cible à atteindre.

    Returns:
        list[tuple]: Liste des coordonnées (x, y) représentant le chemin trouvé du départ à la cible.
    """
    open_list = []
    heapq.heappush(open_list, start)
    start.g = 0
    start.h = heuristic(start, end)
    start.f = start.h

    while open_list:
        current = heapq.heappop(open_list)

        if current == end:
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]

        successors = identify_successors(grid, current, end)
        for successor in successors:
            heapq.heappush(open_list, successor)

    return []  # Aucun chemin trouvé


if __name__ == '__main__':
    app = QApplication(sys.argv)
    snake_game = GameBoard()
    sys.exit(app.exec_())
