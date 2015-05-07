import sys
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from game import GameSpace

class Command(LineReceiver):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        print 'Connected to server.'

    def lineReceived(self, line):
        print line
        line = line.rstrip()
        tokens = line.split(',')
        if tokens[0] == 'MAP':
            #                 [world size] [tiles]
            self.gs.initWorld(tokens[1:3], tokens[3:])
        elif tokens[0] == 'POS1':
            #                  tankType,  ( position )
            self.gs.initPlayer(tokens[1], tokens[2:])
        elif tokens[0] == 'POS2':
            #                 tankType,  ( position )
            self.gs.initEnemy(tokens[1], tokens[2:])
        elif tokens[0] == 'MOVE':
            self.gs.enemy.key_handler(int(tokens[1])) # keycode
        elif tokens[0] == 'FIRE':
            self.gs.fire(self.gs.enemy)
        elif tokens[0] == 'TURR':
            self.gs.enemy.turret_direction = int(tokens[1]) # turret direction
        elif tokens[0] == 'QUIT':
            print 'The other player left.'
        #else:
            #print line

class CommandFactory(ClientFactory):
    def __init__(self, gs):
        self.gs = gs
        self.connection = None

    def buildProtocol(self, addr):
        self.connection = Command(self.gs)
        return self.connection

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.'

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: $ python client.py <address> <port>'
        sys.exit()
    gs = GameSpace()
    factory = CommandFactory(gs)
    reactor.connectTCP(sys.argv[1], int(sys.argv[2]), factory)
    gs.connection = factory.connection
    reactor.run()
