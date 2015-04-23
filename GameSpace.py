import sys
import os
import os.path
import math
import pygame
from pygame.locals import *

class GameSpace:
	def main(self):
		# 1) basic intialization
		pygame.init()
		pygame.mixer.init()


		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0
		
		self.screen = pygame.display.set_mode(self.size)

		# 2) set up game objects
		self.clock = pygame.time.Clock()

		# 3) start game loop
		while 1:
			# 4) clock tick regulation (framerate)
			self.clock.tick(60)
			
			# 5) this is where you would handle user inputs


			# 6) send a tick to every game object!
			
			# 7) and finally, display the game objects
			self.screen.fill(self.black)

			pygame.display.flip()
