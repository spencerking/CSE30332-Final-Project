# Tank subclass for networked player

from tank import Tank

class Enemy(Tank):
    def tick(self):
        # Get the mouse direction from the other player
        self.turret_direction = 0

        super(Enemy, self).tick()
