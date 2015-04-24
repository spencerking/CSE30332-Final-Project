# Spencer King, David Wu, 4/23/15, CSE 30332

import pygame
from pygame.locals import *

class Tank(pygame.sprite.Sprite):
	def __init__(self, gs=None):
		pygame.sprite.Sprite.__init__(self)

		#pass the tank type to determine which image to use

		self.direction = 0
		self.tank_image = pygame.image.load('tank/tank%d.bmp' % self.direction)
		self.turret_image = pygame.image.load('tank/turret%d.bmp' % self.direction)

		#look into masking instead
		self.rect = self.image.get_rect()

		self.fire_sound = pygame.mixer.Sound("tank_fire.wav")
		self.move_sound = pygame.mixer.Sound("tank_move.wav")

	def tick(self):
		# get the moues x and y position for the turret
		mx, my = pygame.mouse.get_pos()

		#probably reuse the rotation stuff from the pygame primer here

	def move(self, keycode):
		#8 directions
		#maybe get two key presses at the same time for non-cardinal directions
		return
