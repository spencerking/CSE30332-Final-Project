# Spencer King, David Wu, 4/23/15, CSE 30332

import pygame
import math
from pygame.locals import *

class Tank(pygame.sprite.Sprite):
	def __init__(self, type, gs=None):
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.type = type

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

		self.tank_image = pygame.image.load('tank/'+self.type+'/tank%d.bmp' % self.direction)
		self.turret_image = pygame.image.load('tank/'+self.type+'/turret%d.bmp' % self.direction)

		#look into masking instead
		self.rect = self.tank_image.get_rect()

		self.fire_sound = pygame.mixer.Sound("audio/tank_fire.wav")
		self.move_sound = pygame.mixer.Sound("tank_move.wav")

		# Stores which tile the tank is currently on, updates as the tank moves
		self.curr_tile = [0, 0]

		self.px = self.rect.center[0]
		self.py = self.rect.center[1]
		self.f_angle = 0

	def tick(self):
		# Determine the turret image & fire direction based on mouse position
		mx, my = pygame.mouse.get_pos()
		theta = math.atan2(my-self.py, mx-self.px)
		angle = (90 - ((theta*180)/math.pi)) % 360

		if 22.5 < angle <= 67.5:
			self.turret_image = pygame.image.load('tank/'+self.type+'/turret7.bmp')
		elif 67.5 < angle <= 112.5:
			self.turret_image = pygame.image.load('tank/'+self.type+'/turret6.bmp')
		elif 112.5 < angle <= 157.5:
			self.turret_image = pygame.image.load('tank/'+self.type+'/turret5.bmp')
		elif 157.5 < angle <= 202.5:
			self.turret_image = pygame.image.load('tank/'+self.type+'/turret4.bmp')
		elif 202.5 < angle <= 247.5:
			self.turret_image = pygame.image.load('tank/'+self.type+'/turret3.bmp')
		elif 247.5 < angle <= 292.5:
			self.turret_image = pygame.image.load('tank/'+self.type+'/turret2.bmp')
		elif 292.5 < angle <= 337.5:
			self.turret_image = pygame.image.load('tank/'+self.type+'/turret1.bmp')
		else:
			self.turret_image = pygame.image.load('tank/'+self.type+'/turret0.bmp')

		# Draw tank and turret
		self.gs.screen.blit(self.tank_image, self.rect)
		self.gs.screen.blit(self.turret_image, self.turret_image.get_rect())

	def move(self, orientation):
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
