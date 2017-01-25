import pygame

from camera import Camera
from constants import BLACK, RED, WHITE, SCREEN_DIMENSIONS, TILE_SIZE
from peep import Peep
from vector import Vector2d
from world import World


class ExitGame(Exception):
    pass


class Game(object):

    def __init__(self):
        self.screen = None
        self.clock = None
        self.camera = None
        self.world = None
        self.font = None

        self.peeps = []

    def start(self):
        self.setup()
        self.run()

    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
        self.clock = pygame.time.Clock()

        self.camera = Camera(TILE_SIZE, *SCREEN_DIMENSIONS)
        self.world = World()
        self.font = get_default_font()

    def exit_game(self):
        raise ExitGame('Thanks for playing!')

    def run(self):
        self.screen.fill(BLACK)
        pygame.display.flip()

        # make testing objects
        self.start_point = Vector2d(13, 12)
        self.end_point = Vector2d(12, 10)

        self.make_testing_path(self.start_point, self.end_point)

        the_peep = Peep()
        the_peep.tile_coords = self.start_point
        self.peeps.append(the_peep)

        # used for debug only
        self.mouse_pos = Vector2d(pygame.mouse.get_pos())
        self.x = self.y = -1

        # main loop
        while True:
            self.screen.fill(BLACK)

            self.handle_input()

            self.camera.draw(self.world, TILE_SIZE, self.screen)

            self.draw_debug_text(self.mouse_pos, self.x, self.y)

            for peep in self.peeps:
                peep.draw(self.screen, self.camera.get_tile_bounds(),
                          self.camera)

            pygame.display.set_caption("Py_park - FPS: %s" %
                                       self.clock.get_fps())

            pygame.display.flip()
            self.clock.tick(60)

    def handle_input(self):
        # maybe use .poll() to get the first and clear the queue?
        # depends how i want it to work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_input(event)
            elif event.type == pygame.KEYDOWN:
                self.keyboard_input(event)

    def mouse_input(self, event):
        left, middle, right = pygame.mouse.get_pressed()

        if left:
            mouse_pos = pygame.mouse.get_pos()
            tile_vector2d = self.camera.get_corresponding_tile(
                mouse_pos[0], mouse_pos[1])
            self.world[tile_vector2d.x][tile_vector2d.y].clicked()
            self.x, self.y = tile_vector2d.x, tile_vector2d.y
        elif right:
            path = self.world.compute_path(self.start_point, self.end_point)
            for i in path:
                self.world.get_tile(i).colour = RED

    def keyboard_input(self, event):
        if event.key == pygame.K_ESCAPE:
            self.exit_game()
        if event.key == pygame.K_RIGHT:
            self.peeps[0].Vector2d.x -= TILE_SIZE
            self.camera.move_tile(1, 0)
        if event.key == pygame.K_LEFT:
            self.peeps[0].Vector2d.x += TILE_SIZE
            self.camera.move_tile(-1, 0)
        if event.key == pygame.K_UP:
            self.peeps[0].Vector2d.y += TILE_SIZE
            self.camera.move_tile(0, -1)
        if event.key == pygame.K_DOWN:
            self.peeps[0].Vector2d.y -= TILE_SIZE
            self.camera.move_tile(0, 1)

    def make_testing_path(self, start_point, end_point):
        self.world.get_tile(start_point).make_path()
        self.world.get_tile(Vector2d(12, 12)).make_path()
        self.world.get_tile(Vector2d(11, 12)).make_path()
        self.world.get_tile(Vector2d(10, 12)).make_path()
        self.world.get_tile(Vector2d(10, 11)).make_path()
        self.world.get_tile(Vector2d(10, 10)).make_path()
        self.world.get_tile(Vector2d(11, 10)).make_path()
        self.world.get_tile(end_point).make_path()

        self.world.get_tile(start_point).colour = WHITE
        self.world.get_tile(end_point).colour = BLACK

    def draw_debug_text(self, mouse_pos, x, y):
        # mouse position
        font_surface1 = self.font.render(
            "x: %s, y: %s" % pygame.mouse.get_pos(), True, (255, 120, 255),
            BLACK)
        self.screen.blit(font_surface1, (0, 0))

        # tile bounds
        tile_bounds = self.camera.get_tile_bounds()
        font_surface2 = self.font.render(
            "viewing - top left: %s, bottom right: %s" %
            (tile_bounds.topleft, tile_bounds.bottomright), True,
            (255, 120, 255), BLACK)
        self.screen.blit(font_surface2, (0, font_surface1.get_height()))

        # mouse x,y last clicked
        font_surface3 = self.font.render(
            "mouse last clicked - x: %s, y: %s" %
            (mouse_pos[0], mouse_pos[1]), True, (255, 120, 255), BLACK)
        self.screen.blit(
            font_surface3,
            (0, font_surface2.get_height() + font_surface1.get_height()))

        # mouse tile last clicked
        font_surface4 = self.font.render(
            "mouse tile last clicked - x: %s, y: %s" % (x, y), True,
            (255, 120, 255), BLACK)
        self.screen.blit(font_surface4, (0, font_surface1.get_height()*3))

        # mouse tile hover
        hover_tile = self.camera.get_corresponding_tile(
            *pygame.mouse.get_pos())
        font_surface5 = self.font.render(
            "mouse tile hover - x: %s, y: %s" % (hover_tile.x, hover_tile.y),
            True, (255, 120, 255), BLACK)
        self.screen.blit(font_surface5, (0, font_surface1.get_height()*4))


def get_default_font():
    default_font = pygame.font.get_default_font()
    return pygame.font.Font(default_font, 12)


if __name__ == '__main__':
    Game().start()
