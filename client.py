import sys
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from game import GameSpace

class Client():
    def __init__(self, args):
        self.serverAddress = args[1]
        self.serverPort = int(args[2])
        self.factory = ClientConnFactory(self)
        self.gs = GameSpace(self, args[3])
        reactor.connectTCP(self.serverAddress, self.serverPort, self.factory)

    def run(self):
        gameLoop = LoopingCall(self.gs.main)
        gameLoop.start(1.0/60)
        reactor.run()

class ClientConnFactory(ClientFactory):
    def __init__(self, client):
        self.client = client

    def buildProtocol(self, addr):
        newConn = ClientConnProtocol(self)
        self.client.connection = newConn
        return newConn

class ClientConnProtocol(LineReceiver):
    def __init__(self, factory):
        self.gs = factory.client.gs

    def connectionMade(self):
        print 'Connected to server'

    def lineReceived(self, line):
        print line
        line = line.rstrip()
        tokens = line.split(',')
        if tokens[0] == 'MAP':
            #                 [world size] [tiles]
            self.gs.initWorld(tokens[1:3], tokens[3:])
        elif tokens[0] == 'POS1':
            self.gs.initPlayer(tokens[1:]) # [x, y]
        elif tokens[0] == 'POS2':
            #                 tankType,  ( position )
            self.gs.initEnemy(tokens[1], ( int(tokens[2]), int(tokens[3]) ))
        elif tokens[0] == 'MOVE':
            self.gs.enemy.key_handler(int(tokens[1])) # keycode
        elif tokens[0] == 'FIRE':
            self.gs.fire(self.gs.enemy)
        elif tokens[0] == 'TURR':
            self.gs.enemy.turret_direction = int(tokens[1]) # turret direction
        elif tokens[0] == 'QUIT':
            print 'The other player left'
            # TODO: cleanly exit

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: $ python client.py <address> <port> <tank type>'
        print 'Tank types are "blue", "green", and "red"'
        sys.exit()
    client = Client(sys.argv)
    client.run()
