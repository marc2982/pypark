from tile import Tile
from vector import Vector2d

MAP_SIZE = 100

STRAIGHT_MOVE_COST = 10
DIAGONAL_MOVE_COST = 14
GRASS_MOVE_COST = 20

class Map(object):
    def __init__(self):
        # dimensions are in tiles
        self.width = self.height = MAP_SIZE
        self.size = (self.width, self.height)
        #TODO: performance: convert this to a 1d array (http://www.reddit.com/r/gamedev/comments/jgv2m/performance_of_arrays/)
        self.tiles = [[Tile() for x in range(self.width)] for y in range(self.height)]

    def __getitem__(self, key):
        return self.tiles[key]

    def getTile(self, p):
        return self[p.x][p.y]

    def aStar(self, start, end, cutCorners=False):
        openSet = []
        closedSet = []

        # add starting node
        currentNode = Node()
        currentNode.Vector2d = start
        currentNode.g = 0
        currentNode.h = self.heuristicDistanceToGoal(start, end)
        currentNode.f = currentNode.g + currentNode.h
        currentNode.parent = currentNode.Vector2d  # set parent = starting because it doesn't matter

        openSet.append(currentNode)

        while openSet:
            # get node with lowest f score
            node = sorted(openSet, key=lambda n: n.f)[0]

            # if node is destination, we are done
            if node.Vector2d == end:
                closedSet.append(node)
                return self.reconstructPath(closedSet)

            # remove node from the open set and put it in the closed set
            openSet.remove(node)
            closedSet.append(node)

            orthogonal = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            diagonal = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
            direction = orthogonal + diagonal

            for nodePosition in direction:
                n = Node()
                n.Vector2d = Vector2d(node.Vector2d.x + nodePosition[0], node.Vector2d.y + nodePosition[1])

                #is the node in bounds and walkable? if not, move to next node
                if not self.getTile(n.Vector2d).isPath:
                    continue

                if not cutCorners:
                    if nodePosition in diagonal and \
                       (not self[n.Vector2d.x+nodePosition[0]][n.Vector2d.y].isPath or \
                        not self[n.Vector2d.x][n.Vector2d.y+nodePosition[1]].isPath):
                        continue

                # i is the index in direction, the first 4 are orthogonal, the last 4 are diagonal
                if nodePosition in orthogonal:   # straight moves
                    if self[n.Vector2d.x][n.Vector2d.y].isPath:
                        newG = node.g + STRAIGHT_MOVE_COST
                    else:
                        newG = node.g + GRASS_MOVE_COST
                else:   # diagonal moves
                    newG = node.g + DIAGONAL_MOVE_COST

                # if the newg is the same as the current one, move to the next node
                if newG == node.g:
                    continue

                # is n in open set?
                inOpenSet = None
                for aNode in openSet:
                    if aNode.Vector2d == n.Vector2d:
                        inOpenSet = aNode
                        break

                # if in the open set and has a lower g score than the new one, move to the next tile
                if inOpenSet and inOpenSet.g <= newG:
                    continue

                # is n in closed set?
                inClosedSet = None
                for aNode in closedSet:
                    if aNode.Vector2d == n.Vector2d:
                        inClosedSet = aNode
                        break

                # if in the open set and has a lower g score than the new one, move to the next tile
                if inClosedSet and inClosedSet.g <= newG:
                    continue

                n.parent = node.Vector2d
                n.g = newG
                n.h = self.heuristicDistanceToGoal(n.Vector2d, end)
                n.f = n.g + n.h

                openSet.append(n)

        return self.reconstructPath(closedSet)

    def heuristicDistanceToGoal(self, p, dest):
        return STRAIGHT_MOVE_COST * (abs(dest.x - p.x) + abs(dest.y - p.y))

    def reconstructPath(self, theSet):
        theSet = list(theSet)
        node = theSet[-1]
        theSet.reverse()

        for n in theSet:
            if node.parent == n.Vector2d or n == node:
                node = n
            else:
                theSet.remove(n)

        return [n.Vector2d for n in theSet]

class Node:
    def __init__(self):
        self.f = 0
        self.g = 0
        self.h = 0
        self.Vector2d = None
        self.parent = None

    def __str__(self):
        return "< node: " + str(self.Vector2d) + "; f=%s; g=%s; h=%s" % (self.f, self.g, self.h) + "; parent: " + str(self.parent) + " >"
    def __repr__(self):
        return self.__str__()
