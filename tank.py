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
		self.id = None

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

	def tick(self):
		# Update tank image based on current direction
		self.tank_image = pygame.image.load('tank/'+self.type+'/tank%d.png' % self.direction)

		self.turret_image = pygame.image.load('tank/'+self.type+'/turret%d.png' % self.turret_direction)

		# Draw tank and turret
		self.gs.screen.blit(self.tank_image, self.rect)
		self.gs.screen.blit(self.turret_image, self.rect)

	#compares a tank tile position against that tile on the world map
	def check_tile(self, x_coord, y_coord):
		#if world_map tile can't be moved to, return false
		#else update tank properties and return true

		#don't want to go outside the map
		if x_coord < 0 or y_coord < 0:
			return False
		elif x_coord > 6 or y_coord > 6:
			return False

		check_list = self.gs.world.map[x_coord]
		if check_list[y_coord].type == 2:
			return False
		else:
			return True  

	#Need to compare the world map tile against the tile the tank will be moving to
	#This will determine current properties of the tank or whether that tile can be moved to
	def move(self, orientation):
		if orientation == 'forward':
			if self.direction == 0:
				dx = 0
				dy = -120
				
			elif self.direction == 1:
				dx = 80
				dy = -60

			elif self.direction == 2:
				dx = 160
				dy = 0

			elif self.direction == 3:
				dx = 80
				dy = 60

			elif self.direction == 4:
				dx = 0
				dy = 120

			elif self.direction == 5:
				dx = -80
				dy = 60

			elif self.direction == 6:
				dx = -160
				dy = 0

			elif self.direction == 7:
				dx = -80
				dy = -60

		elif orientation == 'backward':
			if self.direction == 0:
				dx = 0
				dy = 120

			elif self.direction == 1:
				dx = -80
				dy = 60

			elif self.direction == 2:
				dx = -160
				dy = 0

			elif self.direction == 3:
				dx = -80
				dy = -60

			elif self.direction == 4:
				dx = 0
				dy = -120

			elif self.direction == 5:
				dx = 80
				dy = -60

			elif self.direction == 6:
				dx = 160
				dy = 0

			elif self.direction == 7:
				dx = 80
				dy = 60


		#Calculate the new tile for the tank

		#down right diagonal 
		if dx > 0 and dy > 0:
			x = self.curr_tile[0] + 1
			y = self.curr_tile[1]

		#up left diagonal
		elif dx < 0 and dy < 0:
			x = self.curr_tile[0] - 1
			y = self.curr_tile[1]

		#up right diagonal 
		elif dx > 0 and dy < 0:
			x = self.curr_tile[0]
			y = self.curr_tile[1] - 1

		#down left diagonal 
		elif dx < 0 and dy > 0:
			x = self.curr_tile[0]
			y = self.curr_tile[1] + 1

		#straight right
		elif dx > 0 and dy == 0:
			x = self.curr_tile[0] + 1
			y = self.curr_tile[1] + 1

		#straight left
		elif dx < 0 and dy == 0:
			x = self.curr_tile[0] - 1
			y = self.curr_tile[1] - 1

		#straight down
		elif dx == 0 and dy > 0:
			x = self.curr_tile[0] + 1
			y = self.curr_tile[1] + 1

		#straight up
		elif dx == 0 and dy < 0:
			x = self.curr_tile[0] - 1
			y = self.curr_tile[1] - 1


		if self.check_tile(x, y):
			self.curr_tile = (x, y)
			self.rect = self.rect.move(dx,dy)

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
		self.id = None

		if self.direction == 0:
			self.dy = 5
		elif self.direction == 1:
			self.dx = -4
			self.dy = 3
		elif self.direction == 2:
			self.dx = -5
		elif self.direction == 3:
			self.dx = -4
			self.dy = -3
		elif self.direction == 4:
			self.dy = -5
		elif self.direction == 5:
			self.dx = 4
			self.dy = -3
		elif self.direction == 6:
			self.dx = 5
		elif self.direction == 7:
			self.dx = 4
			self.dy = 3

	def tick(self):
		self.rect = self.rect.move(self.dx, self.dy)
		self.gs.screen.blit(self.image, self.rect)
