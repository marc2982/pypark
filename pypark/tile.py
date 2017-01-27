import pygame

from constants import (
    GRASS_COLOUR, BORDER_COLOUR, PATH_COLOUR, TILE_SIZE, SHOP_COLOUR)


class Tile(object):

    def __init__(self):
        self.colour = GRASS_COLOUR
        self.is_path = False
        self.is_shop = False
        self.H = None

    def clicked(self):
        self.change()

    def change(self):
        if self.is_path:
            self.make_grass()
        else:
            self.make_path()

    def toggle_shop(self):
        if self.is_shop:
            self.make_grass()
        else:
            self.make_shop()
        return self.is_shop

    def make_path(self):
        self.is_path = True
        self.is_shop = False
        self.set_colour()

    def make_grass(self):
        self.is_path = False
        self.is_shop = False
        self.set_colour()

    def make_shop(self):
        self.is_path = False
        self.is_shop = True
        self.set_colour()

    def set_colour(self):
        """Sets tile colour."""
        if self.is_path:
            self.colour = PATH_COLOUR
        elif self.is_shop:
            self.colour = SHOP_COLOUR
        else:
            self.colour = GRASS_COLOUR

    def draw(self, x, y, screen):
        """Draw the tile on the given screen.

        Note that x and y are screen coordinates and not world coordinates.
        """
        r = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        if self.colour:
            r = screen.fill(self.colour, r)
        pygame.draw.rect(screen, BORDER_COLOUR, r, 1)
