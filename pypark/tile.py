import pygame
from constants import GRASS_COLOUR, BORDER_COLOUR, PATH_COLOUR

TILE_SIZE = 20

class Tile(object):
    def __init__(self):
        self.colour = GRASS_COLOUR
        self.isPath = False
        self.H = None

    def clicked(self):
        self.change()

    def change(self):
        if self.isPath:
            self.makeGrass()
        else:
            self.makePath()

    def makePath(self):
        self.isPath = True
        self.colour = PATH_COLOUR

    def makeGrass(self):
        self.isPath = False
        #self.colour = GRASS_COLOUR
        self.colour = (150, 240, 150)

    def draw(self, tileSize, x, y, screen):
        r = pygame.Rect(x, y, tileSize, tileSize)
        if self.colour:
            r = screen.fill(self.colour, r)
        pygame.draw.rect(screen, BORDER_COLOUR, r, 1)
