# Spencer King, David Wu, 4/23/15, CSE 30332

import pygame
from pygame.locals import *

class Tank(pygame.sprite.Sprite):
	def __init__(self, type, gs=None):
		pygame.sprite.Sprite.__init__(self)

		self.dir_str = None

		#stores which tile the tank is currently on, updates as the tank moves
		self.curr_tile = [0, 0]

		#direction is initially NW, 1 is N, 2 NE, etc.
		self.direction = 0
		self.px = 0
		self.py = 0
		self.f_angle = 0

		'''
				NW
	W						N


SW									NE


	S						E
				SE				
		'''

		#pass the tank type to determine which image to use
		if type == 1:
			self.dir_str = 'green'
			self.health = 150
			self.strength = 5
		elif type == 2:
			self.dir_str = 'blue'
			self.health = 100
			self.strength = 10
		elif type == 3:
			self.dir_str = 'red'
			self.health = 75
			self.strength = 15

		self.tank_image = pygame.image.load('tank/' + self.dir_str + '/tank%d.bmp' % self.direction)
		self.turret_image = pygame.image.load('tank/' + self.dir_str + '/turret%d.bmp' % self.direction)

		# keep original image to limit resize errors
		self.orig_turret = self.turret_image

		#look into masking instead
		self.rect = self.image.get_rect()

		self.fire_sound = pygame.mixer.Sound("tank_fire.wav")
		self.move_sound = pygame.mixer.Sound("tank_move.wav")

	def tick(self):
		# get the moues x and y position for the turret
		mx, my = pygame.mouse.get_pos()

		#probably reuse the rotation stuff from the pygame primer here
		rot_angle = 360 - math.atan2(my-self.py, mx-self.px)*180/math.pi
		fire_angle = math.atan2(my-self.py, mx-self.px)
		rot_img = pygame.transform.rotate(self.orig_turret, rot_angle)
		self.turret_image = self.rot_img
		self.f_angle = fire_angle

	def move(self, orientation):
		#MOVING THE TANK FORWARD
		if orientation == "forward":
			if self.direction == 0:
				self.rect = self.rect.move(0,-45)
				py -= 45
			elif self.direction == 1:
				self.rect = self.rect.move(91,-45)
				px += 91
				py -= 45
			elif self.direction == 2:
				self.rect = self.rect.move(91,0)
				px += 91
			elif self.direction == 3:
				self.rect = self.rect.move(91,45)
				px += 91
				py += 45
			elif self.direction == 4:
				self.rect = self.rect.move(0,45)
				py += 45
			elif self.direction == 5:
				self.rect = self.rect.move(-91,45)
				px -= 91
				py += 45
			elif self.direction == 6:
				self.rect = self.rect.move(-91,0)
				px -= 91
			elif self.direction == 7:
				self.rect = self.rect.move(-91,-45)
				px -= 91
				py -= 45
		#MOVING THE TANK BACKWARD
		elif orientation == "backward":
			if self.direction == 0:
				self.rect = self.rect.move(0,45)
				py += 45
			elif self.direction == 1:
				self.rect = self.rect.move(-91,45)
				px -= 91
				py += 45
			elif self.direction == 2:
				self.rect = self.rect.move(-91,0)
				px -= 91
			elif self.direction == 3:
				self.rect = self.rect.move(-91,-45)
				px -= 91
				py -= 45
			elif self.direction == 4:
				self.rect = self.rect.move(0,-45)
				py -= 45
			elif self.direction == 5:
				self.rect = self.rect.move(91,-45)
				px += 91
				py -= 45
			elif self.direction == 6:
				self.rect = self.rect.move(91,0)
				px += 91
			elif self.direction == 7:
				self.rect = self.rect.move(91,45)
				px += 91
				py += 45

	#fires a bullet
	def fire(self):
		self.fire_sound.play()

	def key_handler(self, keycode):
		#8 directions
		#up and down move forward and back, right and left change direction
		if keycode == K_DOWN:
			self.move("backward")
		elif keycode == K_UP:
			self.move("forward")
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
	def __init__(self, angle, x, y, gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("laser.png")
		self.rect = self.image.get_rect()

		self.l_start_x = x
		self.l_start_y = y
		self.rect.centerx = self.l_start_x
		self.rect.centery = self.l_start_y
		self.l_angle = angle
		self.speed = 3

	def tick(self):
		l_x_pos = self.speed*math.cos(self.l_angle)
		l_y_pos = self.speed*math.sin(self.l_angle)
		self.rect.centerx = self.rect.centerx + l_x_pos
		self.rect.centery = self.rect.centery + l_y_pos
