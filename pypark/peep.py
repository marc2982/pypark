import pygame
from vector import Vector2d
from constants import BLUE

class Peep(object):
    def __init__(self):
        self.Vector2d = None
        self.tileCoords = None

    def draw(self, screen, viewableRange, camera):
        if not self.Vector2d:
            if self.tileCoords:
                self.Vector2d = Vector2d(self.tileCoords.x*camera.tileSize, self.tileCoords.y*camera.tileSize)
            else:
                self.Vector2d = Vector2d(320*camera.tileSize, 240*camera.tileSize)

        if self.tileCoords and \
           self.tileCoords.x in range(viewableRange.left, viewableRange.right) and \
           self.tileCoords.y in range(viewableRange.top, viewableRange.bottom):
            pygame.draw.circle(screen, BLUE, (self.Vector2d.x+10, self.Vector2d.y+10), 5, 0)
