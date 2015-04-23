# David Wu, 4/23/15, CSE 30332

import pygame
from pygame.locals import *

class World:
    def __init__(self, gs=None):
        self.gs = gs

        # Generate 2d array of tiles
        for 


class Tile(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image