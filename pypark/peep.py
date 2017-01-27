import random

from constants import BLUE, TILE_SIZE, RED
from vector import Vector2d

import pygame


class Peep(object):

    def __init__(self, position):
        # position is world coordinates
        self.position = position
        self.destination_tile = None
        self.path = None
        self.speed = 1
        self.acting_at_destination = True
        self.acting_ticks = 0

    @property
    def current_tile(self):
        return self.position / TILE_SIZE

    def update(self, world):
        """Called every tick to update peep."""
        if self.acting_at_destination:
            self.acting_ticks += 1
            if self.acting_ticks == 60:  # arbitrary waiting period
                self.acting_ticks = 0
                self.acting_at_destination = False
        elif self.destination_tile:
            self._move_along_path()
        else:
            self.choose_new_destination(world)

    def _move_along_path(self):
        """Move along the current path to the destination."""
        current_tile = self.current_tile  # calculate once

        if current_tile != self.destination_tile and not self.path:
            raise Exception('no path to destination :(')

        next_tile = self.path[0]
        if current_tile == next_tile:
            # TODO: go to middle of tile only if destination coords aren't set
            tile_middle = next_tile * TILE_SIZE + TILE_SIZE/2

            # TODO: won't work with speed != 1 cause of overshooting
            if self.position == tile_middle:
                if current_tile == self.destination_tile:
                    self.destination_tile = None
                    self.path = None
                    self.acting_at_destination = True
                    return

                # get new tile
                self.path.pop(0)
                normal_vector = None
            else:
                normal_vector = (
                    tile_middle - self.position).normalized().intify()
        else:
            normal_vector = next_tile - current_tile

        # move if necessary
        if normal_vector:
            self.position += normal_vector * self.speed

    def choose_new_destination(self, world):
        """Choose a new destination tile."""
        if world.directory.shops:
            destination = random.choice(world.directory.shops)
            # TODO: Compute target tile to be the path that touches it.
            # Currently hardcoded tile directly below shop to be target tile
            # (because you can't walk on shop tile).
            self.destination_tile = destination.position + Vector2d(0, 1)
            # TODO: add destination coords
            self.path = world.pathfinder.compute(
                self.current_tile, self.destination_tile)

    def draw(self, camera, screen):
        if camera.rect.collidepoint(self.position.tuple):
            screen_pos = self.position - camera.position
            pygame.draw.circle(
                screen, BLUE,
                (screen_pos.x, screen_pos.y), 5, 0)
