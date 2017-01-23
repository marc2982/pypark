import pygame
from vector import Vector2d

class Camera(object):
    #TODO: performance: only calculate tileOffset and tileBounds after camera movement
    def __init__(self, tileSize, w, h):
        self.tileSize = tileSize
        self.Vector2d = Vector2d(0,0)
        self.size = Vector2d(w, h)

    def move(self, dx, dy):
        #TODO: figure this out
        #dx = lib.clamp(0, dx, MAP_SIZE * self.tileSize)
        #dy = lib.clamp(0, dy, MAP_SIZE * self.tileSize)

        self.Vector2d.x += dx
        self.Vector2d.y += dy

    def moveTile(self, tileX, tileY):
        self.move(tileX * self.tileSize, tileY * self.tileSize)

    def jumpTo(self, x, y):
        self.Vector2d.x = x
        self.Vector2d.y = y

    def getTileOffset(self):
        return Vector2d(self.Vector2d.x % self.tileSize, self.Vector2d.y % self.tileSize)

    def getTileBounds(self):
        x = int(self.Vector2d.x / self.tileSize)
        y = int(self.Vector2d.y / self.tileSize)

        w = int(self.size.x / self.tileSize) + 2
        h = int(self.size.y / self.tileSize) + 2

        if x % self.tileSize != 0:
            w += 1
        if y % self.tileSize != 0:
            h += 1

        return pygame.Rect(x, y, w, h)

    def getCorrespondingTile(self, x, y):
        bounds = self.getTileBounds()
        offset = self.getTileOffset()
        #return (bounds.left+offset[0])/self.tileSize, (bounds.top+offset[1])/self.tileSize
        return Vector2d((x+offset.x)/self.tileSize+bounds.left, (y+offset.y)/self.tileSize+bounds.top)

    def draw(self, theMap, tileSize, screen):
        x = y = 0
        bounds = self.getTileBounds()
        offset = self.getTileOffset()

        for tileY in xrange(bounds.top, bounds.bottom):
            for tileX in xrange(bounds.left, bounds.right):
                tile = theMap[tileX][tileY]
                tile.draw(tileSize,
                          (x*tileSize) - offset.x,
                          (y*tileSize) - offset.y,
                          screen)
                x += 1
            x = 0
            y += 1
