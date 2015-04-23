# David Wu, 4/23/15, CSE 30332

import pygame
from pygame.locals import *
from random import randint

class World:
    def __init__(self, height, width, gs=None):
        self.gs = gs
        self.map = []

        # Generate 2d array of tiles
        for i in range(0, height):
            self.map.append([])
            for j in range(0, width):
                self.map[i].append(Tile(randint(0, 2), self))

    def tick(self):
        for i in range(0, height):
            for tile in self.map[i]:
                self.gs.screen.blit(tile.image, tile.rect)

class Tile(pygame.sprite.Sprite):
    def __init__(self, imageid, world=None):
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
