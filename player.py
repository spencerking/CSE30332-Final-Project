# Tank subclass for local player

import pygame
import math
from tank import Tank

class Player(Tank):
    def tick(self):
        # Determine direction based on mouse position
        mx, my = pygame.mouse.get_pos()
        theta = math.atan2(my-self.rect.center[1], mx-self.rect.center[0])
        self.angle = (90 - ((theta*180)/math.pi)) % 360

        # Update turret image based on mouse direction
        if 22.5 < self.angle <= 67.5:
            self.turret_direction = 7
        elif 67.5 < self.angle <= 112.5:
            self.turret_direction = 6
        elif 112.5 < self.angle <= 157.5:
            self.turret_direction = 5
        elif 157.5 < self.angle <= 202.5:
            self.turret_direction = 4
        elif 202.5 < self.angle <= 247.5:
            self.turret_direction = 3
        elif 247.5 < self.angle <= 292.5:
            self.turret_direction = 2
        elif 292.5 < self.angle <= 337.5:
            self.turret_direction = 1
        else:
            self.turret_direction = 0

        # Send turret direction to other player
        self.gs.client.transport.write('TUR,' + self.turret_direction + '\r\n')

        super(Player, self).tick()
