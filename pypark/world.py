from constants import TILE_SIZE
from directory import Directory
from pathfinding import Pathfinding
from tile import Tile

import pygame

WORLD_SIZE = 100


class World(object):

    def __init__(self, pathfinder=None, directory=None):
        self.width = WORLD_SIZE  # tiles
        self.height = WORLD_SIZE  # tiles
        self.width_coords = self.width * TILE_SIZE
        self.height_coords = self.height * TILE_SIZE
        # TODO: performance:
        # convert this to a 1d array
        # http://www.reddit.com/r/gamedev/comments/jgv2m/performance_of_arrays/
        self.tiles = [
            [Tile() for x in range(self.width)] for y in range(self.height)]
        self.pathfinder = pathfinder or Pathfinding(self)
        self.directory = directory or Directory()

    def __getitem__(self, key):
        return self.tiles[key]

    def get_tile(self, p):
        return self[p.x][p.y]

    def iter_tiles(self):
        for tile_y in range(self.height):
            for tile_x in range(self.width):
                yield self[tile_x][tile_y]

    def draw(self, camera, screen):
        camera_rect = camera.rect
        for tile_y in range(self.height):
            for tile_x in range(self.width):
                world_x = tile_x * TILE_SIZE
                world_y = tile_y * TILE_SIZE
                rect = pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)
                if camera_rect.contains(rect):
                    screen_x = world_x - camera.position.x
                    screen_y = world_y - camera.position.y
                    tile = self[tile_x][tile_y]
                    tile.draw(screen_x, screen_y, screen)

    def compute_path(self, start, end, cut_corners=False):
        return self.pathfinder.compute(start, end, cut_corners=cut_corners)
