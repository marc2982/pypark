import pygame
import map
from peep import Peep
from camera import Camera
from vector import Vector2d
from constants import PATH_COLOUR, BLACK, RED, WHITE

TILE_SIZE = 10

def run():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    run = True
    screen.fill(BLACK)
    pygame.display.flip()

    defaultFont = pygame.font.get_default_font()
    f = pygame.font.Font(defaultFont, 12)

    theMap = map.Map()

    startPoint = Vector2d(13, 12)
    endPoint = Vector2d(12, 10)

    thePeep = Peep()
    thePeep.tileCoords = startPoint

    # set path
    theMap.getTile(startPoint).makePath()
    theMap.getTile(Vector2d(12, 12)).makePath()
    theMap.getTile(Vector2d(11, 12)).makePath()
    theMap.getTile(Vector2d(10, 12)).makePath()
    theMap.getTile(Vector2d(10, 11)).makePath()
    theMap.getTile(Vector2d(10, 10)).makePath()
    theMap.getTile(Vector2d(11, 10)).makePath()
    theMap.getTile(endPoint).makePath()

    theMap.getTile(startPoint).colour = WHITE
    theMap.getTile(endPoint).colour = BLACK

    mousePos = Vector2d(pygame.mouse.get_pos())
    camera = Camera(TILE_SIZE, 640, 480)

    x = y = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                leftButton, middleButton, rightButton = pygame.mouse.get_pressed()

                if leftButton:
                    mousePos = pygame.mouse.get_pos()
                    tileVector2d = camera.getCorrespondingTile(mousePos[0], mousePos[1])
                    theMap[tileVector2d.x][tileVector2d.y].clicked()
                if rightButton:
                    path = theMap.aStar(startPoint, endPoint)
                    for x in path:
                        theMap.getTile(x).colour = RED

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_RIGHT:
                    thePeep.Vector2d.x -= TILE_SIZE
                    camera.moveTile(1, 0)
                if event.key == pygame.K_LEFT:
                    thePeep.Vector2d.x += TILE_SIZE
                    camera.moveTile(-1, 0)
                if event.key == pygame.K_UP:
                    thePeep.Vector2d.y += TILE_SIZE
                    camera.moveTile(0, -1)
                if event.key == pygame.K_DOWN:
                    thePeep.Vector2d.y -= TILE_SIZE
                    camera.moveTile(0, 1)

        screen.fill(BLACK)

        # draw viewable range
        camera.draw(theMap, TILE_SIZE, screen)

        # draw text top left
        fontSurface1 = f.render("x: %s, y: %s" % pygame.mouse.get_pos(), True, (255, 120, 255), (0,0,0))
        screen.blit(fontSurface1, (0, 0))

        tileBounds = camera.getTileBounds()
        fontSurface2 = f.render("viewing - top left: %s, bottom right: %s" % (tileBounds.topleft, tileBounds.bottomright), True, (255, 120, 255), (0,0,0))
        screen.blit(fontSurface2, (0, fontSurface1.get_height()))

        fontSurface3 = f.render("mouse last clicked - x: %s, y: %s" % (mousePos[0], mousePos[1]), True, (255, 120, 255), (0,0,0))
        screen.blit(fontSurface3, (0, fontSurface2.get_height()+fontSurface1.get_height()))

        fontSurface4 = f.render("mouse tile last clicked - x: %s, y: %s" % (x, y), True, (255, 120, 255), (0,0,0))
        screen.blit(fontSurface4, (0, fontSurface1.get_height()*3))

        hoverTile = camera.getCorrespondingTile(*pygame.mouse.get_pos())
        fontSurface5 = f.render("mouse tile hover - x: %s, y: %s" % (hoverTile.x, hoverTile.y), True, (255, 120, 255), (0,0,0))
        screen.blit(fontSurface5, (0, fontSurface1.get_height()*4))

        # draw peep
        thePeep.draw(screen, tileBounds, camera)

        # set caption
        pygame.display.set_caption("PyPark - FPS: %s" % clock.get_fps())

        # flip buffer and set fps
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    run()
