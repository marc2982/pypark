import pygame

from constants import (
    GRASS_COLOUR, BORDER_COLOUR, PATH_COLOUR, TILE_SIZE, SHOP_COLOUR)


class Tile(object):

    def __init__(self):
        self.is_grass = False
        self.is_path = False
        self.is_shop = False

    def draw(self, x, y, screen):
        """Draw the tile on the given screen.

        Note that x and y are screen coordinates and not world coordinates.
        """
        r = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        if self.colour:
            r = screen.fill(self.colour, r)
        pygame.draw.rect(screen, BORDER_COLOUR, r, 1)


class GrassTile(Tile):

    def __init__(self):
        super(GrassTile, self).__init__()
        self.is_grass = True
        self.colour = GRASS_COLOUR
        self.walkable = True
        self.debug = '-'


class PathTile(Tile):

    def __init__(self):
        super(PathTile, self).__init__()
        self.is_path = True
        self.colour = PATH_COLOUR
        self.walkable = True
        self.debug = 'p'


class ShopTile(Tile):

    def __init__(self):
        super(ShopTile, self).__init__()
        self.is_shop = True
        self.colour = SHOP_COLOUR
        self.walkable = False
        self.debug = 's'
