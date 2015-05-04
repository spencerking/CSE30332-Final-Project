# David Wu, Spencer King, 4/23/15, CSE 30332
# With help from http://gamedevelopment.tutsplus.com/tutorials/creating-isometric-worlds-a-primer-for-game-developers--gamedev-6511
import pygame
from pygame.locals import *
from random import randint

class World:
    def __init__(self, height, width, gs=None):
        self.gs = gs
        self.height = height
        self.width = width
        self.tile_height = 163
        self.tile_width = 123
        self.map = []

        # Generate 2d array of tiles
        for i in range(0, self.height):
            self.map.append([])
            for j in range(0, self.width):
                imageid = randint(0, 2)
                pos = iso_from_cartesian(80*(i), 80*(j))
                self.map[i].append(Tile(imageid, pos, self))

    def tick(self):
        for i in range(0, self.height):
            for tile in self.map[i]:
                self.gs.screen.blit(tile.image, tile.rect)

class Tile(pygame.sprite.Sprite):
    def __init__(self, imageid, pos, world=None):
        pygame.sprite.Sprite.__init__(self)
        self.world = world
        self.type = imageid
        randid = randint(1, 3)
        if imageid == 0:
            filename = 'grass%d.png' % randid
        elif imageid == 1:
            filename = 'gravel%d.png' % randid
        else:
            filename = 'water%d.png' % randid
        self.image = pygame.image.load('tiles/%s' % filename)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)

def iso_from_cartesian(x, y):
    return ((x+250) - (y-250), ((x+250) + (y-250))/1.33)
