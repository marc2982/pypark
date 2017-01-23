import pygame
from constants import GRASS_COLOUR, BORDER_COLOUR, PATH_COLOUR

TILE_SIZE = 20


class Tile(object):
    def __init__(self):
        self.colour = GRASS_COLOUR
        self.is_path = False
        self.H = None

    def clicked(self):
        self.change()

    def change(self):
        if self.is_path:
            self.make_grass()
        else:
            self.make_path()

    def make_path(self):
        self.is_path = True
        self.colour = PATH_COLOUR

    def make_grass(self):
        self.is_path = False
        self.colour = GRASS_COLOUR

    def draw(self, tile_size, x, y, screen):
        r = pygame.Rect(x, y, tile_size, tile_size)
        if self.colour:
            r = screen.fill(self.colour, r)
        pygame.draw.rect(screen, BORDER_COLOUR, r, 1)
