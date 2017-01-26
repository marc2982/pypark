from constants import TILE_SIZE
from lib import clamp
from vector import Vector2d

import pygame


class Camera(object):

    def __init__(self, world, position, w, h):
        self.world = world
        # position is top left of camera in world coordinates
        self.position = position or Vector2d(0, 0)  # top left of camera
        self.width = w
        self.height = h

        self.max_x = self.world.width_coords - self.width
        self.max_y = self.world.height_coords - self.height

    @property
    def rect(self):
        x = self.position.x
        y = self.position.y
        return pygame.Rect(x, y, self.width, self.height)

    def move_tile(self, tile_x, tile_y):
        """Move by increments of given number of tiles."""
        self.move(tile_x * TILE_SIZE, tile_y * TILE_SIZE)

    def move(self, dx, dy):
        """Move the camera by the given dx and dy distances."""
        new_x = clamp(self.position.x + dx, 0, self.max_x)
        new_y = clamp(self.position.y + dy, 0, self.max_y)
        self.position = Vector2d(new_x, new_y)

    def get_world_tile(self, x, y):
        """Return the corresponding world tile to the given screen coords."""
        pos = self.get_world_tile_indexes(x, y)
        return self.world[pos.x][pos.y]

    def get_world_coords(self, x, y):
        """Return the corresponding world coords to the given screen coords."""
        return self.position + Vector2d(x, y)

    def get_world_tile_indexes(self, x, y):
        """Return the corresponding world tiles to the given screen coords."""
        pos = self.get_world_coords(x, y)
        return Vector2d(pos.x / TILE_SIZE, pos.y / TILE_SIZE)
