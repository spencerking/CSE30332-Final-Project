# David Wu, Spencer King, 4/23/15, CSE 30332
# With help from http://gamedevelopment.tutsplus.com/tutorials/creating-isometric-worlds-a-primer-for-game-developers--gamedev-6511

import pygame
from pygame.locals import *
from random import randint

class World:
    def __init__(self, size, tiles, gs):
        self.gs = gs
        self.height = size[0]
        self.width = size[1]
        self.tile_height = 163
        self.tile_width = 123
        self.map = []

        # Generate 2d array of tiles
        for i in range(0, self.height):
            self.map.append([])
            for j in range(0, self.width):
                imageid = tiles[i*self.height + j]
                pos = iso_from_cartesian(80*(i), 80*(j))
                self.map[i].append(Tile(imageid, pos))

    def tick(self):
        for i in range(0, self.height):
            for tile in self.map[i]:
                self.gs.screen.blit(tile.image, tile.rect)

    def valid_tile(self, tanktype, x, y):
        if x < 0 or y < 0 or x > self.height or y > self.width:
            return False

        row = self.map[x]
        if row[y].type == 'water' and tanktype != 'blue':
            return False
    
    def tile_bonus(self, tanktype, x, y):
        row = self.map[x]
        if row[y].type == 'gravel' and tanktype == 'red':
            return 5
        elif row[y].type == 'grass' and tanktype == 'green':
            return 5
        else:
            return 0

    @staticmethod
    def iso_from_cartesian(x, y):
        return ((x+250) - (y-250), ((x+250) + (y-250))/1.33)

class Tile(pygame.sprite.Sprite):
    def __init__(self, imageid, pos):
        pygame.sprite.Sprite.__init__(self)
        randid = randint(1, 3)
        if imageid == 0:
            self.type = 'grass'
            filename = 'grass%d.png' % randid
        elif imageid == 1:
            self.type = 'gravel'
            filename = 'gravel%d.png' % randid
        else:
            self.type = 'water'
            filename = 'water%d.png' % randid
        self.image = pygame.image.load('tiles/%s' % filename)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)
