# Spencer King, David Wu, 4/23/15, CSE 30332

import pygame
from pygame.locals import *
from world import World # iso_from_cartesian

class Tank(pygame.sprite.Sprite):
	def __init__(self, tanktype, pos, gs):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.tank_type = tanktype
		self.fire_sound = pygame.mixer.Sound('audio/tank_fire.wav')
		self.move_sound = pygame.mixer.Sound('audio/tank_move.wav')
		self.curr_tile = pos
		self.tile_bonus = 0 # Bonus damage based on the current tile

		# Direction is initially NW, 1 is N, 2 NE, etc.
		self.direction = 0
		#				NW
		#		W				N
		#
		#
		#	SW						NE
		#
		#
		#		S				E
		#				SE

		# Initialize based on tank type
		if self.tank_type == 'green':
			self.health = 140
			self.strength = 5
		elif self.tank_type == 'blue':
			self.health = 100
			self.strength = 10
		elif self.tank_type == 'red':
			self.health = 75
			self.strength = 15

		self.tank_image = pygame.image.load('tank/'+self.tank_type+'/tank%d.png' % self.direction)
		self.turret_image = pygame.image.load('tank/'+self.tank_type+'/turret%d.png' % self.direction)
		self.rect = self.tank_image.get_rect()

		displayed_pos = World.iso_from_cartesian(int(pos[0])*80-8, int(pos[1])*80-8)
		self.rect = self.rect.move(displayed_pos)

	def tick(self):
		# Update tank image based on current direction
		self.tank_image = pygame.image.load('tank/'+self.tank_type+'/tank%d.png' % self.direction)
		self.turret_image = pygame.image.load('tank/'+self.tank_type+'/turret%d.png' % self.turret_direction)

		# Draw tank and turret
		self.gs.screen.blit(self.tank_image, self.rect)
		self.gs.screen.blit(self.turret_image, self.rect)

	'''
	Need to compare the world map tile against the tile the tank will be moving to
	This will determine current properties of the tank or whether that tile can be moved to
	'''
	def move(self, orientation):
		dx = 0
		dy = 0
		if orientation == 'forward':
			direction = self.direction
		elif orientation == 'backward':
			direction = (self.direction + 4) % 8

		if direction == 0:
			dx = 0
			dy = -120
			x = self.curr_tile[0] - 1
			y = self.curr_tile[1] - 1
		elif direction == 1:
			dx = 80
			dy = -60
			x = self.curr_tile[0]
			y = self.curr_tile[1] - 1
		elif direction == 2:
			dx = 160
			dy = 0
			x = self.curr_tile[0] + 1
			y = self.curr_tile[1] - 1
		elif direction == 3:
			dx = 80
			dy = 60
			x = self.curr_tile[0] + 1
			y = self.curr_tile[1]
		elif direction == 4:
			dx = 0
			dy = 120
			x = self.curr_tile[0] + 1
			y = self.curr_tile[1] + 1
		elif direction == 5:
			dx = -80
			dy = 60
			x = self.curr_tile[0]
			y = self.curr_tile[1] + 1
		elif direction == 6:
			dx = -160
			dy = 0
			x = self.curr_tile[0] - 1
			y = self.curr_tile[1] + 1
		elif direction == 7:
			dx = -80
			dy = -60
			x = self.curr_tile[0] - 1
			y = self.curr_tile[1]

		if self.gs.world.valid_tile(self.tank_type, x, y):
			self.curr_tile = (x, y)
			self.rect = self.rect.move(dx, dy)
			self.tile_bonus = self.gs.world.tile_bonus(self.tank_type, x, y)

			# Animation doesn't work
			# Based on https://www.pygame.org/docs/tut/MoveIt.html

			# print dx/100.0
			# for i in range(100):
			# 	mov_x = dx/100
			# 	mov_y = dy/100
			#  	self.rect = self.rect.move(mov_x,mov_y)
			#  	self.gs.screen.blit(self.tank_image, self.rect)
			#  	self.gs.screen.blit(self.turret_image, self.rect)

	# GameSpace instance creates and manages the bullet object
	def key_handler(self, keycode):
		# 8 directions
		# Up and down move forward and back, right and left change direction
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
		return

# GameSpace instance creates and manages the bullet object
class Bullet(pygame.sprite.Sprite):
	def __init__(self, firing_tank, gs):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.owner = firing_tank
		self.image = pygame.image.load('tank/laser.png')
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(firing_tank.rect.center)
		self.direction = firing_tank.direction
		self.damage = firing_tank.strength + firing_tank.tile_bonus

		self.dx = 0
		self.dy = 0
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
