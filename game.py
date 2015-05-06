# David Wu, Spencer King, 4/23/15, CSE 30332

import sys
from random import randint
import pygame
from pygame.locals import *
from world import World
from tank import Tank, Bullet
from player import Player
from enemy import Enemy

class GameSpace:
    def __init__(self, client, tankType):
        self.client = client

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Tanks')
        pygame.key.set_repeat(1, 50)
        self.size = self.width, self.height = 1200, 800
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.sprites = []

        # Tell server this player's starting position
        self.client.connection.transport.write('POS,' + self.player.curr_tile[0] +','+ self.player.curr_tile[1])

    def initWorld(self, size, tiles):
        self.world = World(size, tiles, self)
        self.sprites.append(self.world)

    def initPlayer(self, position):
        self.player = Player()
        self.sprites.append(self.player)

    def initEnemy(self, tankType, position):
        self.enemy = Enemy(tankType, position, self)
        self.sprites.append(self.world)

    def fire(self, firing_tank):
        bullet = Bullet(firing_tank, self)
        self.sprites.append(bullet)

    def main(self):
        # Run
        while 1:
            self.clock.tick(60)

            # Handle user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    self.player.key_handler(event.key)

                    # Send key event to other player
                    self.client.transport.write('MOV,' + event.key)

                if event.type == MOUSEBUTTONDOWN:
                    self.fire(self.player)

                    self.sprites.append(bullet)
                    self.player.fire_sound.play()

                    # Send mouse event to other player
                    self.client.transport.write('FIR,' + self.player.turret_direction)

            self.screen.fill(self.black)

            # Collision detection
            # TODO: MAKE SURE TO SEND DAMAGE
            for s in self.sprites:
                s.tick()
                if isinstance(s, Bullet):
                    if s.rect.colliderect(self.player.rect) and s.id != self.player.id:
                        self.player.health -= s.damage
                        self.sprites.remove(s)
                    if s.rect.colliderect(self.enemy.rect) and s.id != self.enemy.id:
                        self.enemy.health -= s.damage
                        self.sprites.remove(s)

            pygame.display.flip()
