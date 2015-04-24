# David Wu, 4/23/15, CSE 30332

import pygame
from pygame.locals import *
from random import randint

class World:
    def __init__(self, height, width, gs=None):
        self.gs = gs
        self.height = height
        self.width = width
        self.tile_height = 91
        self.tile_width = 46
        self.map = []

        # Generate 2d array of tiles
        for i in range(0, self.height):
            self.map.append([])
            for j in range(0, self.width):
                imageid = randint(0, 2)
                pos = iso_from_cartesian(self.tile_height*i, self.tile_width*j)
                self.map[i].append(Tile(imageid, pos, self))

    def tick(self):
        for i in range(0, self.height):
            for tile in self.map[i]:
                self.gs.screen.blit(tile.image, tile.rect)

class Tile(pygame.sprite.Sprite):
    def __init__(self, imageid, pos, world=None):
        pygame.sprite.Sprite.__init__(self)
        self.world = world
        if imageid == 0:
            filename = 'grass.png'
        elif imageid == 1:
            filename = 'gravel.png'
        else:
            filename = 'water.png'
        self.image = pygame.image.load('tiles/%s' % filename)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)

def iso_from_cartesian(x, y):
    return (x - y, (x - y)/2)
