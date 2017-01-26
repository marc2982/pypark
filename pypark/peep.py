import pygame

from constants import BLUE, TILE_SIZE


class Peep(object):

    def __init__(self, position):
        # position is world coordinates
        self.position = position
        self.destination_tile = None
        self.path = None
        self.speed = 1

    def update(self):
        if self.destination_tile:
            current_tile = self.position / TILE_SIZE

            if current_tile != self.destination_tile and not self.path:
                raise Exception('no path to destination :(')

            next_tile = self.path[0]
            if current_tile == next_tile:
                # go to middle of tile
                tile_middle = next_tile * TILE_SIZE + TILE_SIZE/2

                # TODO: won't work with speed != 1 cause of overshooting
                if self.position == tile_middle:
                    if current_tile == self.destination_tile:
                        self.destination_tile = None
                        self.path = None
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

    def draw(self, camera, screen):
        if camera.rect.collidepoint(self.position.tuple):
            screen_pos = self.position - camera.position
            pygame.draw.circle(
                screen, BLUE,
                (screen_pos.x, screen_pos.y), 5, 0)
