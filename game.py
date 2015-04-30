# David Wu, Spencer King, 4/23/15, CSE 30332

import sys
import pygame
from pygame.locals import *
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from world import World
from tank import Tank, Bullet
from player import Player
from enemy import Enemy

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

        self.world = World(7, 7, self)
        self.sprites.append(self.world)
        # TODO: check if tank location is not water
        self.player = Player('green', (0,0), self)
        self.sprites.append(self.player)
        self.enemy = Enemy('blue', (5,5), self)
        self.sprites.append(self.enemy)

        while 1:
            self.clock.tick(60)

            # Handle user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                #For KEYDOWN events pass the map list to player as well
                #This allows for tile property comparisons
                if event.type == KEYDOWN:
                    self.player.key_handler(event.key, self.world.map)
                    # TODO: send key event to other player
                if event.type == MOUSEBUTTONDOWN:
                    bullet = Bullet(self.player.turret_direction, self.player.rect[0], self.player.rect[1], self)
                    self.sprites.append(bullet)
                    self.player.fire_sound.play()
                    # TODO: send mouse event to other player

            self.screen.fill(self.black)

            for s in self.sprites:
                s.tick()

            pygame.display.flip()
