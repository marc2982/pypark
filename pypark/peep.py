import pygame

from constants import BLUE, TILE_SIZE

OFFSET = TILE_SIZE / 2


class Peep(object):

    def __init__(self, position):
        # position is world coordinates
        self.position = position

    def update(self):
        pass

    def draw(self, camera, screen):
        if camera.rect.collidepoint(self.position.tuple):
            screen_pos = self.position - camera.position
            pygame.draw.circle(
                screen, BLUE,
                (screen_pos.x + OFFSET, screen_pos.y + OFFSET), 5, 0)
