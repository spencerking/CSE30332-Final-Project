# David Wu, Spencer King, 4/23/15, CSE 30332

import sys
import pygame
from pygame.locals import *
from world import World
from tank import Tank, Bullet
from player import Player
from enemy import Enemy
from random import randint

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


        self.test = Player("red", (0,0), self)
        self.sprites.append(self.test)
        
        #randomly position tanks and make sure the position is valid
        x = 1
        while x == 1: 
            p_randx = randint(0,6)
            p_randy = randint(0,6)
            if self.test.check_tile(p_randx, p_randy):
                 x = 2

        while x == 2: 
            e_randx = randint(0,6)
            e_randy = randint(0,6)
            if self.test.check_tile(e_randx, e_randy):
                 x = 3

        self.sprites.remove(self.test)

        #instantiate tanks with random colors
        '''
        rand_color = randint(1,3)
        if rand_color == 1:
            self.player = Player('green', (p_randx,p_randy), self)
            self.sprites.append(self.player)
        elif rand_color == 2:
            self.player = Player('red', (p_randx,p_randy), self)
            self.sprites.append(self.player)
        elif rand_color == 3:
            self.player = Player('blue', (p_randx,p_randy), self)
            self.sprites.append(self.player)

        rand_color = randint(1,3)
        if rand_color == 1:
            self.enemy = Enemy('green', (e_randx,e_randy), self)
            self.sprites.append(self.enemy)
        elif rand_color == 2:
            self.enemy = Enemy('red', (e_randx,e_randy), self)
            self.sprites.append(self.enemy)
        elif rand_color == 3:
            self.enemy = Enemy('blue', (e_randx,e_randy), self)
            self.sprites.append(self.enemy)
        '''
        
        self.player = Player('green', (p_randx,p_randy), self)
        self.sprites.append(self.player)
        self.enemy = Enemy('blue', (e_randx,e_randy), self)
        self.sprites.append(self.enemy)
        
        #CHANGE LATER
        self.player.id = 0
        self.enemy.id = 1


        while 1:
            self.clock.tick(60)

            # Handle user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    self.player.key_handler(event.key)
                    # TODO: send key event to other player
                if event.type == MOUSEBUTTONDOWN:
                    bullet = Bullet(self.player.turret_direction, self.player.rect[0], self.player.rect[1], self)
                    #CHANGE THIS ID LATER
                    bullet.id = 0
                    
                    self.sprites.append(bullet)
                    self.player.fire_sound.play()

                    # TODO: send mouse event to other player

            self.screen.fill(self.black)

            #collision detection
            for s in self.sprites:
                s.tick()
                if isinstance(s, Bullet):
                    if s.rect.colliderect(self.player.rect) and s.id != self.player.id:
                        self.sprites.remove(s)
                    if s.rect.colliderect(self.enemy.rect) and s.id != self.enemy.id:
                        self.sprites.remove(s)


            pygame.display.flip()
