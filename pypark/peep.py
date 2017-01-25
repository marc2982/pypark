import pygame

from constants import BLUE
from vector import Vector2d


class Peep(object):
    def __init__(self):
        self.Vector2d = None
        self.tile_coords = None

    def update(self):
        pass

    def draw(self, screen, viewable_range, camera):
        if not self.Vector2d:
            if self.tile_coords:
                self.Vector2d = Vector2d(self.tile_coords.x*camera.tile_size, self.tile_coords.y*camera.tile_size)
            else:
                self.Vector2d = Vector2d(320*camera.tile_size, 240*camera.tile_size)

        if self.tile_coords and \
           self.tile_coords.x in range(viewable_range.left, viewable_range.right) and \
           self.tile_coords.y in range(viewable_range.top, viewable_range.bottom):
            pygame.draw.circle(screen, BLUE, (self.Vector2d.x+10, self.Vector2d.y+10), 5, 0)
