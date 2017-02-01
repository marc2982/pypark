"""Contains pathfinding-related functionality.

This algorithm is adapted from the pseudocode located here:
https://en.wikipedia.org/w/index.php?title=A*_search_algorithm&oldid=761920249

It was then modified to support cutting corners and various movement costs.
"""

STRAIGHT_MOVE_COST = 10
DIAGONAL_MOVE_COST = 14
GRASS_MOVE_COST = 40


class Pathfinding(object):

    """Pathfinding using A*."""

    def __init__(self, world):
        self.world = world
        self.orthogonal = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.diagonal = [(1, -1), (1, 1), (-1, 1), (-1, -1)]

    def compute(self, start, end, cut_corners=False):
        neighbour_vectors = self.orthogonal
        if cut_corners:
            neighbour_vectors += self.diagonal

        open_set = []  # nodes haven't tried yet
        closed_set = []  # nodes we've tried
        came_from = {}  # optimal path

        # add starting node
        start_node = Node()
        start_node.position = start
        start_node.h = self.heuristic_distance_to_goal(start, end)
        open_set.append(start_node)

        while open_set:
            # get node with lowest f score
            current = sorted(open_set, key=lambda n: n.f)[0]

            # if node is destination, we are done
            if current.position == end:
                closed_set.append(current)
                return self.reconstruct_path(came_from, current)

            # remove node from the open set and put it in the closed set
            # because we have tried it out
            open_set.remove(current)
            closed_set.append(current)

            # loop through all neighbouring tiles
            for neighbour_vector in neighbour_vectors:
                neighbour = Node()
                neighbour.position = current.position + neighbour_vector

                # if we have already evaluated this tile, ignore
                if self.in_set(neighbour, closed_set):
                    continue

                # is the node in bounds and walkable? if not, ignore
                tile = self.world.get_tile(neighbour.position)
                if not tile or not tile.is_walkable:
                    continue

                # calculate new g
                new_g = self.calculate_new_g(
                    tile, current, neighbour_vector in self.diagonal)

                # add to open set if not already in
                if not self.in_set(neighbour, open_set):
                    open_set.append(neighbour)
                elif new_g >= neighbour.g:
                    continue  # This is not a better path

                came_from[neighbour] = current
                neighbour.g = new_g
                neighbour.h = self.heuristic_distance_to_goal(
                    neighbour.position, end)

        return []  # could not find a path

    def in_set(self, n, set_):
        for node in set_:
            if n.position == node.position:
                return True
        return False

    def calculate_new_g(self, tile, current, diagonal_movement):
        if tile.is_path:
            new_g = current.g + STRAIGHT_MOVE_COST
        elif tile.is_grass:
            new_g = current.g + GRASS_MOVE_COST
        else:
            raise Exception('uh oh!')

        if diagonal_movement:
            new_g += DIAGONAL_MOVE_COST

        return new_g

    def heuristic_distance_to_goal(self, p, dest):
        return STRAIGHT_MOVE_COST * (abs(dest.x - p.x) + abs(dest.y - p.y))

    def reconstruct_path(self, came_from, current):
        path = [current.position]
        while current in came_from:
            current = came_from[current]
            path.append(current.position)
        path.reverse()
        return path


class Node:

    """A node in the path."""

    __slots__ = ('g', 'h', 'position')

    def __init__(self):
        self.g = 0  # cost of the path from the start node to here
        self.h = 0  # heuristic estimate from here to goal node
        self.position = None

    @property
    def f(self):
        """Return estimated cost still remaining to goal."""
        return self.g + self.h

    def __str__(self):
        return 'Node(g=%s, h=%s, f=%s, position=%s)' % (
            self.g, self.h, self.f, self.position)

    __repr__ = __str__

    def __hash__(self):
        return hash((self.position.x, self.position.y))
