from mock import Mock
from unittest2 import TestCase, skip

from pypark.world import World
from pypark.vector import Vector2d
from pypark import pathfinding


class TestPathfinding(TestCase):

    def setUp(self):
        # TODO: fix circular dependency world/pathfinder
        self.world = World(5, 5, pathfinder=None, directory=None)
        self.pathfinder = pathfinding.Pathfinding(self.world)

    def test_begin_end_square_same(self):
        """Begin and end square are the same.

        -----
        -----
        --B--
        -----
        -----

        TODO: is this result desired? Should it, in fact, return an empty path?
        """
        begin = Vector2d(2, 2)
        end = Vector2d(2, 2)

        self.world.make_path(Vector2d(2, 2))
        path = self.pathfinder.compute(begin, end)

        self.assertEqual([
            Vector2d(2, 2),
            ], path
        )

    def test_one_tile_path(self):
        """begin and end tile one tile apart.

        -----
        --E--
        --B--
        -----
        -----
        """
        begin = Vector2d(2, 2)
        end = Vector2d(1, 2)

        self.world.make_path(Vector2d(1, 2))
        self.world.make_path(Vector2d(2, 2))

        path = self.pathfinder.compute(begin, end)

        self.assertEqual([
            Vector2d(2, 2),
            Vector2d(1, 2),
            ], path
        )

    def test_l_shaped_path_touch_edge(self):
        """L-shaped path.

        -----
        -----
        --B--
        --p--
        --pE-
        """
        begin = Vector2d(2, 2)
        end = Vector2d(3, 4)

        self.world.make_path(Vector2d(2, 2))
        self.world.make_path(Vector2d(2, 3))
        self.world.make_path(Vector2d(2, 4))
        self.world.make_path(Vector2d(3, 4))

        path = self.pathfinder.compute(begin, end)

        self.assertEqual([
            Vector2d(2, 2),
            Vector2d(2, 3),
            Vector2d(2, 4),
            Vector2d(3, 4),
            ], path
        )

    @skip('TODO: currently broken')
    def test_no_concrete_path_to_end(self):
        """No concrete path to end point. Peep should take the grass.

        -----
        --B--
        -----
        --E--
        -----
        """
        begin = Vector2d(2, 1)
        end = Vector2d(2, 3)

        path = self.pathfinder.compute(begin, end)

        self.assertEqual([
            Vector2d(2, 1),
            Vector2d(2, 2),
            Vector2d(2, 3),
            ], path
        )

    @skip('TODO: currently broken')
    def test_no_walkable_path_to_end(self):
        """No walkable path to end point. Peep cannot make it to end.

        -----
        --B--
        SSSSS
        --E--
        -----
        """
        begin = Vector2d(2, 1)
        end = Vector2d(2, 3)

        self.world.make_path(Vector2d(0, 2))
        self.world.make_path(Vector2d(1, 2))
        self.world.make_path(Vector2d(2, 2))
        self.world.make_path(Vector2d(3, 2))
        self.world.make_path(Vector2d(4, 2))

        path = self.pathfinder.compute(begin, end)

        self.assertEqual([], path)

    def test_take_shortest_path(self):
        """Test that the peep takes the shortest path available.

        -----
        -Bpp-
        -p-p-
        -pEp-
        -----
        """
        begin = Vector2d(1, 1)
        end = Vector2d(2, 3)

        # begin and end
        self.world.make_path(Vector2d(1, 1))
        self.world.make_path(Vector2d(2, 3))

        # short path
        self.world.make_path(Vector2d(1, 2))
        self.world.make_path(Vector2d(1, 3))

        # long path
        self.world.make_path(Vector2d(2, 1))
        self.world.make_path(Vector2d(3, 1))
        self.world.make_path(Vector2d(3, 2))
        self.world.make_path(Vector2d(3, 3))

        path = self.pathfinder.compute(begin, end)

        self.assertEqual([
            Vector2d(1, 1),
            Vector2d(1, 2),
            Vector2d(1, 3),
            Vector2d(2, 3),
            ], path
        )

    @skip('TODO: currently broken')
    def test_take_shortest_path_on_grass(self):
        """Test that the peep takes the grass.

        -----
        -Bpp-
        ---p-
        -Epp-
        -----
        """
        begin = Vector2d(1, 1)
        end = Vector2d(1, 3)

        # begin and end
        self.world.make_path(Vector2d(1, 1))
        self.world.make_path(Vector2d(2, 3))

        # long path
        self.world.make_path(Vector2d(2, 1))
        self.world.make_path(Vector2d(3, 1))
        self.world.make_path(Vector2d(3, 2))
        self.world.make_path(Vector2d(3, 3))
        self.world.make_path(Vector2d(2, 3))

        path = self.pathfinder.compute(begin, end)

        self.assertEqual([
            Vector2d(1, 1),
            Vector2d(1, 2),
            Vector2d(1, 3),
            ], path
        )
