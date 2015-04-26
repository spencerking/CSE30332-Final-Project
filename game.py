# David Wu, Spencer King, 4/23/15, CSE 30332

import sys
import pygame
from pygame.locals import *
from world import World
from tank import Tank

class GameSpace:
    def main(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Tanks')
        pygame.key.set_repeat(1, 50)
        self.size = self.width, self.height = 1200, 800
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.sprites = []

        self.tank = Tank('green', self)
        self.sprites.append(self.tank)
        self.world = World(10, 10, self)
        self.sprites.append(self.world)

        while 1:
            self.clock.tick(60)

            # Handle user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    self.tank.key_handler(event.key)
                if event.type == MOUSEBUTTONDOWN:
                    bullet = self.tank.Bullet(self.tank.f_angle, self.tank.px, self.tank.py)
                    self.sprites.append(bullet)
                    self.tank.fire_sound.play()

            self.screen.fill(self.black)

            for s in self.sprites:
                s.tick()

            pygame.display.flip()
