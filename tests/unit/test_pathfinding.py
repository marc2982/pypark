from mock import Mock
from unittest2 import TestCase

from pypark.world import World
from pypark.vector import Vector2d
from pypark import pathfinding


class TestPathfinding(TestCase):

    def setUp(self):
        # TODO: fix circular dependency world/pathfinder
        self.world = World(5, 5, pathfinder=None, directory=None)
        self.pathfinder = pathfinding.Pathfinding(self.world)

    def test_start_end_square_same(self):
        """Start and end square are the same.

        -----
        -----
        --S--
        -----
        -----

        TODO: is this result desired? Should it, in fact, return an empty path?
        """
        start = Vector2d(2, 2)
        end = Vector2d(2, 2)

        self.world[2][2].make_path()
        path = self.pathfinder.compute(start, end)

        self.assertEqual([
            Vector2d(2, 2),
            ], path
        )
