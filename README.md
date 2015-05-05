# CSE30332-Final-Project

This is the final project for CSE30332 Programming Paradigms at the University of Notre Dame.

**Game Description**

Our game is a two player tank battle game. When the game begins you are prompted to select a tank with specific properties. You will be
placed in a randomly generated map and must defeat the opposing tank. There are three different types of tanks: green, red, and blue. The
green tank has a large amount of health but very little strength, whereas the red tank has lower health but greater strength. Lastly, the
blue tank has average health and strength but is the only tank capable of moving on water tiles. In addition to this, different tile types give strength bonuses to different tanks. The red and green tanks receive strength bonuses when on gravel tiles to make up for their inability to move on water. The grass tiles provide no bonuses to any tank type. 

**Controls**

* Up Arrow - Move forward
* Down Arrow - Move backward
* Right Arrow - Rotate clockwise
* Left Arrow - Rotate counterclockwise
* Mouse Movement - Aim the turret
* Left Mouse Click - Fire

**How to Run**

Start a server by running

$ python server.py

Start a client by running

$ python client.py example.com 9000

**System Requirements**

This game has been tested on Mac OS X 10.9 and 10.10 and Red Hat Enterprise Linux. You need at least Python 2.6 along with the PyGame and Twisted libraries.

**Credits**

Original green tank sprite images from http://www.reinerstilesets.de/2d-grafiken/2d-vehicles/
