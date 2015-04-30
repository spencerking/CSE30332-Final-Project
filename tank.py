# Spencer King, David Wu, 4/23/15, CSE 40332

import pygame
from pygame.locals import *
from world import iso_from_cartesian

class Tank(pygame.sprite.Sprite):
	def __init__(self, type, pos, gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.type = type
		self.fire_sound = pygame.mixer.Sound("audio/tank_fire.wav")
		self.move_sound = pygame.mixer.Sound("tank_move.wav")

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
			self.health = 140
			self.strength = 5
		elif self.type == 'blue':
			self.health = 100
			self.strength = 10
		elif self.type == 'red':
			self.health = 75
			self.strength = 15


		#Load the appropriate tank and turret images
		self.tank_image = pygame.image.load('tank/'+self.type+'/tank%d.png' % self.direction)
		self.turret_image = pygame.image.load('tank/'+self.type+'/turret%d.png' % self.direction)

		#look into masking instead
		self.rect = self.tank_image.get_rect()

		# Stores which tile the tank is currently on, updates as the tank moves
		self.curr_tile = pos

		adj_pos = iso_from_cartesian(pos[0]*80-8, pos[1]*80-8)
		self.rect = self.rect.move(adj_pos)

		self.px = self.rect.center[0]
		self.py = self.rect.center[1]

	def tick(self):
		# Update tank image based on current direction
		self.tank_image = pygame.image.load('tank/'+self.type+'/tank%d.png' % self.direction)

		self.turret_image = pygame.image.load('tank/'+self.type+'/turret%d.png' % self.turret_direction)

		# Draw tank and turret
		self.gs.screen.blit(self.tank_image, self.rect)
		self.gs.screen.blit(self.turret_image, self.rect)

	#compares a tank tile position against that tile on the world map
	def check_tile(self, world_map, tank_tile):
		print "check a tile"
		#TODO if world_map tile can't be moved to, return false
		#else update tank properties and return true

	#Need to compare the world map tile against the tile the tank will be moving to
	#This will determine current properties of the tank or whether that tile can be moved to
	def move(self, orientation, world_map):
		if orientation == 'forward':
			if self.direction == 0:
				#TODO compare the change in pos against the world map tile at that location
				#if water or some obstacle, don't move the rect, otherwise move and update tank properties
				#probably make some method to do this, simpler than putting the conditionals in every case
				self.rect = self.rect.move(0,-120)
			elif self.direction == 1:
				self.rect = self.rect.move(80,-60)
			elif self.direction == 2:
				self.rect = self.rect.move(160,0)
			elif self.direction == 3:
				self.rect = self.rect.move(80,60)
			elif self.direction == 4:
				self.rect = self.rect.move(0,120)
			elif self.direction == 5:
				self.rect = self.rect.move(-80,60)
			elif self.direction == 6:
				self.rect = self.rect.move(-160,0)
			elif self.direction == 7:
				self.rect = self.rect.move(-80,-60)

		elif orientation == 'backward':
			if self.direction == 0:
				self.rect = self.rect.move(0,120)
			elif self.direction == 1:
				self.rect = self.rect.move(-80,60)
			elif self.direction == 2:
				self.rect = self.rect.move(-160,0)
			elif self.direction == 3:
				self.rect = self.rect.move(-80,-60)
			elif self.direction == 4:
				self.rect = self.rect.move(0,-120)
			elif self.direction == 5:
				self.rect = self.rect.move(80,-60)
			elif self.direction == 6:
				self.rect = self.rect.move(160,0)
			elif self.direction == 7:
				self.rect = self.rect.move(80,60)

	# GameSpace instance creates and manages the bullet object
	def fire(self):
		self.fire_sound.play()

	def key_handler(self, keycode, world_map):
		# 8 directions
		# up and down move forward and back, right and left change direction
		if keycode == K_DOWN:
			self.move('backward', world_map)
		elif keycode == K_UP:
			self.move('forward', world_map)
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
