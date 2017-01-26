import pygame

from constants import BLUE, TILE_SIZE


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
                (screen_pos.x, screen_pos.y), 5, 0)
