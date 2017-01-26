import pygame

from constants import GRASS_COLOUR, BORDER_COLOUR, PATH_COLOUR, TILE_SIZE


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

    def draw(self, x, y, screen):
        """Draw the tile on the given screen.

        Note that x and y are screen coordinates and not world coordinates.
        """
        r = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        if self.colour:
            r = screen.fill(self.colour, r)
        pygame.draw.rect(screen, BORDER_COLOUR, r, 1)
