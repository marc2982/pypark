from tile import Tile
from vector import Vector2d

WORLD_SIZE = 100

STRAIGHT_MOVE_COST = 10
DIAGONAL_MOVE_COST = 14
GRASS_MOVE_COST = 20


class World(object):
    def __init__(self):
        # dimensions are in tiles
        self.width = self.height = WORLD_SIZE
        self.size = (self.width, self.height)
        # TODO: performance:
        # convert this to a 1d array
        # http://www.reddit.com/r/gamedev/comments/jgv2m/performance_of_arrays/
        self.tiles = [
            [Tile() for x in range(self.width)] for y in range(self.height)]

    def __getitem__(self, key):
        return self.tiles[key]

    def get_tile(self, p):
        return self[p.x][p.y]

    def compute_path(self, start, end, cut_corners=False):
        return self.a_star(start, end, cut_corners=cut_corners)

    def a_star(self, start, end, cut_corners=False):
        open_set = []
        closed_set = []

        # add starting node
        current_node = Node()
        current_node.Vector2d = start
        current_node.g = 0
        current_node.h = self.heuristic_distance_to_goal(start, end)
        current_node.f = current_node.g + current_node.h
        # set parent = starting because it doesn't matter
        current_node.parent = current_node.Vector2d

        open_set.append(current_node)

        while open_set:
            # get node with lowest f score
            node = sorted(open_set, key=lambda n: n.f)[0]

            # if node is destination, we are done
            if node.Vector2d == end:
                closed_set.append(node)
                return self.reconstruct_path(closed_set)

            # remove node from the open set and put it in the closed set
            open_set.remove(node)
            closed_set.append(node)

            orthogonal = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            diagonal = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
            direction = orthogonal + diagonal

            for node_position in direction:
                n = Node()
                n.Vector2d = Vector2d(node.Vector2d.x + node_position[0],
                                      node.Vector2d.y + node_position[1])

                # is the node in bounds and walkable? if not, move to next node
                if not self.get_tile(n.Vector2d).is_path:
                    continue

                if not cut_corners:
                    if node_position in diagonal and \
                       (not self[n.Vector2d.x+node_position[0]][n.Vector2d.y].is_path or \
                        not self[n.Vector2d.x][n.Vector2d.y+node_position[1]].is_path):
                        continue

                # i is the index in direction
                # the first 4 are orthogonal, the last 4 are diagonal
                if node_position in orthogonal:  # straight moves
                    if self[n.Vector2d.x][n.Vector2d.y].is_path:
                        new_g = node.g + STRAIGHT_MOVE_COST
                    else:
                        new_g = node.g + GRASS_MOVE_COST
                else:  # diagonal moves
                    new_g = node.g + DIAGONAL_MOVE_COST

                # if newg is the same as the current one, move to the next node
                if new_g == node.g:
                    continue

                # is n in open set?
                in_open_set = None
                for a_node in open_set:
                    if a_node.Vector2d == n.Vector2d:
                        in_open_set = a_node
                        break

                # if in the open set and has a lower g score than the new one,
                # move to the next tile
                if in_open_set and in_open_set.g <= new_g:
                    continue

                # is n in closed set?
                in_closed_set = None
                for a_node in closed_set:
                    if a_node.Vector2d == n.Vector2d:
                        in_closed_set = a_node
                        break

                # if in the open set and has a lower g score than the new one,
                # move to the next tile
                if in_closed_set and in_closed_set.g <= new_g:
                    continue

                n.parent = node.Vector2d
                n.g = new_g
                n.h = self.heuristic_distance_to_goal(n.Vector2d, end)
                n.f = n.g + n.h

                open_set.append(n)

        return self.reconstruct_path(closed_set)

    def heuristic_distance_to_goal(self, p, dest):
        return STRAIGHT_MOVE_COST * (abs(dest.x - p.x) + abs(dest.y - p.y))

    def reconstruct_path(self, the_set):
        the_set = list(the_set)
        node = the_set[-1]
        the_set.reverse()

        for n in the_set:
            if node.parent == n.Vector2d or n == node:
                node = n
            else:
                the_set.remove(n)

        return [n.Vector2d for n in the_set]

class Node:
    def __init__(self):
        self.f = 0
        self.g = 0
        self.h = 0
        self.Vector2d = None
        self.parent = None

    def __str__(self):
        return "< node: " + str(self.Vector2d) + \
            "; f=%s; g=%s; h=%s" % (self.f, self.g, self.h) + "; parent: " + \
            str(self.parent) + " >"

    def __repr__(self):
        return self.__str__()
