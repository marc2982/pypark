from mock import Mock
from unittest2 import TestCase

from pypark import pathfinding


class TestPathfinding(TestCase):

    def setUp(self):
        self.pathfinder = pathfinding.Pathfinding(Mock())

    def test_pass(self):
        self.assertTrue(True)
