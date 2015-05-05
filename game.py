# David Wu, Spencer King, 4/23/15, CSE 30332

import sys
import pygame
from pygame.locals import *
from world import World
from tank import Bullet
from player import Player
from enemy import Enemy
from client import Client

class GameSpace:
    def __init__(self, client, player, enemy):
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

        self.world = World(7, 7, self)
        self.sprites.append(self.world)
        # TODO: check if tank location is not water
        self.player = Player(player['type'], player['pos'], self)
        self.sprites.append(self.player)
        self.enemy = Enemy(enemy['type'], enemy['pos'], self)
        self.sprites.append(self.enemy)

        #CHANGE LATER
        self.player.id = 0
        self.enemy.id = 1

    def main(self):
        while 1:
            self.clock.tick(60)

            # Handle user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    self.player.key_handler(event.key)
                    # TODO: send key event to other player
                    self.client.transport.write('MOVE' + self.player.direction)
                if event.type == MOUSEBUTTONDOWN:
                    bullet = Bullet(self.player.turret_direction, self.player.rect[0], self.player.rect[1], self)
                    # CHANGE THIS ID LATER
                    bullet.id = 0
                    
                    self.sprites.append(bullet)
                    self.player.fire_sound.play()

                    # TODO: send mouse event to other player
                    self.client.transport.write('FIRE')

            self.screen.fill(self.black)

            # Collision detection
            for s in self.sprites:
                s.tick()
                if isinstance(s, Bullet):
                    if s.rect.colliderect(self.player.rect) and s.id != self.player.id:
                        self.sprites.remove(s)
                    if s.rect.colliderect(self.enemy.rect) and s.id != self.enemy.id:
                        self.sprites.remove(s)


            pygame.display.flip()
