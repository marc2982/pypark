import pygame
import map
from peep import Peep
from camera import Camera
from vector import Vector2d
from constants import BLACK, RED, WHITE

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600
SCREEN_DIMENSIONS = (SCREEN_HEIGHT, SCREEN_WIDTH)
TILE_SIZE = 20


def run():
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
    clock = pygame.time.Clock()

    run = True
    screen.fill(BLACK)
    pygame.display.flip()

    default_font = pygame.font.get_default_font()
    f = pygame.font.Font(default_font, 12)

    the_map = map.Map()

    start_point = Vector2d(13, 12)
    end_point = Vector2d(12, 10)

    the_peep = Peep()
    the_peep.tile_coords = start_point

    # set path
    the_map.get_tile(start_point).make_path()
    the_map.get_tile(Vector2d(12, 12)).make_path()
    the_map.get_tile(Vector2d(11, 12)).make_path()
    the_map.get_tile(Vector2d(10, 12)).make_path()
    the_map.get_tile(Vector2d(10, 11)).make_path()
    the_map.get_tile(Vector2d(10, 10)).make_path()
    the_map.get_tile(Vector2d(11, 10)).make_path()
    the_map.get_tile(end_point).make_path()

    the_map.get_tile(start_point).colour = WHITE
    the_map.get_tile(end_point).colour = BLACK

    mouse_pos = Vector2d(pygame.mouse.get_pos())
    camera = Camera(TILE_SIZE, *SCREEN_DIMENSIONS)

    x = y = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                left_button, middle_button, right_button = \
                    pygame.mouse.get_pressed()

                if left_button:
                    mouse_pos = pygame.mouse.get_pos()
                    tile_vector2d = camera.get_corresponding_tile(
                        mouse_pos[0], mouse_pos[1])
                    the_map[tile_vector2d.x][tile_vector2d.y].clicked()
                if right_button:
                    path = the_map.a_star(start_point, end_point)
                    for x in path:
                        the_map.get_tile(x).colour = RED

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_RIGHT:
                    the_peep.Vector2d.x -= TILE_SIZE
                    camera.move_tile(1, 0)
                if event.key == pygame.K_LEFT:
                    the_peep.Vector2d.x += TILE_SIZE
                    camera.move_tile(-1, 0)
                if event.key == pygame.K_UP:
                    the_peep.Vector2d.y += TILE_SIZE
                    camera.move_tile(0, -1)
                if event.key == pygame.K_DOWN:
                    the_peep.Vector2d.y -= TILE_SIZE
                    camera.move_tile(0, 1)

        screen.fill(BLACK)

        # draw viewable range
        camera.draw(the_map, TILE_SIZE, screen)

        # draw text top left
        font_surface1 = f.render("x: %s, y: %s" % pygame.mouse.get_pos(), True,
                                 (255, 120, 255), BLACK)
        screen.blit(font_surface1, (0, 0))

        tile_bounds = camera.get_tile_bounds()
        font_surface2 = f.render(
            "viewing - top left: %s, bottom right: %s" %
            (tile_bounds.topleft, tile_bounds.bottomright), True,
            (255, 120, 255), BLACK)
        screen.blit(font_surface2, (0, font_surface1.get_height()))

        font_surface3 = f.render(
            "mouse last clicked - x: %s, y: %s" %
            (mouse_pos[0], mouse_pos[1]), True, (255, 120, 255), BLACK)
        screen.blit(
            font_surface3,
            (0, font_surface2.get_height() + font_surface1.get_height()))

        font_surface4 = f.render(
            "mouse tile last clicked - x: %s, y: %s" % (x, y), True,
            (255, 120, 255), BLACK)
        screen.blit(font_surface4, (0, font_surface1.get_height()*3))

        hover_tile = camera.get_corresponding_tile(*pygame.mouse.get_pos())
        font_surface5 = f.render(
            "mouse tile hover - x: %s, y: %s" % (hover_tile.x, hover_tile.y),
            True, (255, 120, 255), BLACK)
        screen.blit(font_surface5, (0, font_surface1.get_height()*4))

        # draw peep
        the_peep.draw(screen, tile_bounds, camera)

        # set caption
        pygame.display.set_caption("Py_park - FPS: %s" % clock.get_fps())

        # flip buffer and set fps
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    run()
