import pygame
from vector import Vector2d


class Camera(object):
    # TODO: performance:
    # only calculate tile_offset and tile_bounds after camera movement

    def __init__(self, tile_size, w, h):
        self.tile_size = tile_size
        self.Vector2d = Vector2d(0, 0)
        self.size = Vector2d(w, h)

    def move(self, dx, dy):
        # TODO: figure this out
        # dx = lib.clamp(0, dx, WORLD_SIZE * self.tile_size)
        # dy = lib.clamp(0, dy, WORLD_SIZE * self.tile_size)

        self.Vector2d.x += dx
        self.Vector2d.y += dy

    def move_tile(self, tile_x, tile_y):
        self.move(tile_x * self.tile_size, tile_y * self.tile_size)

    def jump_to(self, x, y):
        self.Vector2d.x = x
        self.Vector2d.y = y

    def get_tile_offset(self):
        return Vector2d(
            self.Vector2d.x % self.tile_size,
            self.Vector2d.y % self.tile_size)

    def get_tile_bounds(self):
        x = int(self.Vector2d.x / self.tile_size)
        y = int(self.Vector2d.y / self.tile_size)

        w = int(self.size.x / self.tile_size) + 2
        h = int(self.size.y / self.tile_size) + 2

        if x % self.tile_size != 0:
            w += 1
        if y % self.tile_size != 0:
            h += 1

        return pygame.Rect(x, y, w, h)

    def get_corresponding_tile(self, x, y):
        bounds = self.get_tile_bounds()
        offset = self.get_tile_offset()
        return Vector2d(
            (x + offset.x) / self.tile_size + bounds.left,
            (y + offset.y) / self.tile_size + bounds.top)

    def draw(self, the_world, tile_size, screen):
        x = y = 0
        bounds = self.get_tile_bounds()
        offset = self.get_tile_offset()

        for y, tile_y in enumerate(xrange(bounds.top, bounds.bottom)):
            for x, tile_x in enumerate(xrange(bounds.left, bounds.right)):
                tile = the_world[tile_x][tile_y]
                tile.draw(tile_size,
                          (x*tile_size) - offset.x,
                          (y*tile_size) - offset.y,
                          screen)
