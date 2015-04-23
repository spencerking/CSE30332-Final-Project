# David Wu, 4/23/15, CSE 30332

import pygame
from pygame.locals import *
from world import World
from world import Tile

class GameSpace:
    def main(self):
        pygame.init()
        pygame.display.set_caption('Tanks')
        pygame.key.set_repeat(1, 50)
        self.size = self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.sprites = []

        self.world = World(self)

        while 1:
            self.clock.tick(60)

            # Handle user input
            for event in pygame.event.get():


            for s in self.sprites:
                s.tick()

            self.screen.fill(1, 1, 1)
            for s in self.sprites:
                self.screen.blit(s.image, s.rect)

            pygame.display.flip()