# Spencer King, David Wu, 4/23/15, CSE 30332

import pygame
from pygame.locals import *

class Tank(pygame.sprite.Sprite):
	def __init__(self, type, pos, gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.type = type
		self.fire_sound = pygame.mixer.Sound("audio/tank_fire.wav")
		self.move_sound = pygame.mixer.Sound("tank_move.wav")
		# Stores which tile the tank is currently on, updates as the tank moves
		self.curr_tile = pos
		# TODO: move tank to pos

		# Direction is initially NW, 1 is N, 2 NE, etc.
		self.direction = 0
		'''
			NW
	W				N


SW						NE


	S				E
			SE				
		'''

		# Initialize based on tank type
		if self.type == 'green':
			self.health = 150
			self.strength = 5
		elif self.type == 'blue':
			self.health = 100
			self.strength = 10
		elif self.type == 'red':
			self.health = 75
			self.strength = 15

		self.tank_image = pygame.image.load('tank/'+self.type+'/tank%d.png' % self.direction)
		self.turret_image = pygame.image.load('tank/'+self.type+'/turret%d.png' % self.direction)

		#look into masking instead
		self.rect = self.tank_image.get_rect()
		self.px = self.rect.center[0]
		self.py = self.rect.center[1]

	def tick(self):
		# Update tank image based on current direction
		self.tank_image = pygame.image.load('tank/'+self.type+'/tank%d.png' % self.direction)

		self.turret_image = pygame.image.load('tank/'+self.type+'/turret%d.png' % self.turret_direction)

		# Draw tank and turret
		self.gs.screen.blit(self.tank_image, self.rect)
		self.gs.screen.blit(self.turret_image, self.rect)

	def move(self, orientation):
		if orientation == 'forward':
			if self.direction == 0:
				self.rect = self.rect.move(0,-45)
			elif self.direction == 1:
				self.rect = self.rect.move(50,-45)
			elif self.direction == 2:
				self.rect = self.rect.move(50,0)
			elif self.direction == 3:
				self.rect = self.rect.move(50,45)
			elif self.direction == 4:
				self.rect = self.rect.move(0,45)
			elif self.direction == 5:
				self.rect = self.rect.move(-50,45)
			elif self.direction == 6:
				self.rect = self.rect.move(-50,0)
			elif self.direction == 7:
				self.rect = self.rect.move(-50,-45)

		elif orientation == 'backward':
			if self.direction == 0:
				self.rect = self.rect.move(0,45)
			elif self.direction == 1:
				self.rect = self.rect.move(-50,45)
			elif self.direction == 2:
				self.rect = self.rect.move(-50,0)
			elif self.direction == 3:
				self.rect = self.rect.move(-50,-45)
			elif self.direction == 4:
				self.rect = self.rect.move(0,-45)
			elif self.direction == 5:
				self.rect = self.rect.move(50,-45)
			elif self.direction == 6:
				self.rect = self.rect.move(50,0)
			elif self.direction == 7:
				self.rect = self.rect.move(50,45)

	# GameSpace instance creates and manages the bullet object
	def fire(self):
		self.fire_sound.play()

	def key_handler(self, keycode):
		# 8 directions
		# up and down move forward and back, right and left change direction
		if keycode == K_DOWN:
			self.move('backward')
		elif keycode == K_UP:
			self.move('forward')
		elif keycode == K_RIGHT:
			self.direction += 1
			if self.direction > 7:
				self.direction = 0
		elif keycode == K_LEFT:
			self.direction -= 1
			if self.direction < 0:
				self.direction = 7
		elif keycode == K_SPACE:
			self.fire()
		return

class Bullet(pygame.sprite.Sprite):
	def __init__(self, direction, x, y, gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.image.load('tank/laser.png')
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(self.gs.player.rect.center)
		self.direction = direction
		self.dx = 0
		self.dy = 0
		self.speed = 5

		if self.direction == 0:
			self.dy = self.speed
		elif self.direction == 1:
			self.dx = -self.speed
			self.dy = self.speed
		elif self.direction == 2:
			self.dx = -self.speed
		elif self.direction == 3:
			self.dx = -self.speed
			self.dy = -self.speed
		elif self.direction == 4:
			self.dy = -self.speed
		elif self.direction == 5:
			self.dx = self.speed
			self.dy = -self.speed
		elif self.direction == 6:
			self.dx = self.speed
		elif self.direction == 7:
			self.dx = self.speed
			self.dy = self.speed

	def tick(self):
		self.rect = self.rect.move(self.dx, self.dy)
		self.gs.screen.blit(self.image, self.rect)
