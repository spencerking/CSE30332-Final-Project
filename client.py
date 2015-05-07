import sys
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
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
            self.gs.initPlayer(tokens[1:]) # [x, y]
        elif tokens[0] == 'POS2' and self.gs.enemy is None:
            #                 tankType,  ( position )
            self.gs.initEnemy(tokens[1], ( int(tokens[2]), int(tokens[3]) ))
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

    def buildProtocol(self, addr):
        return Command(self.gs)

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.'

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: $ python client.py <address> <port>'
        sys.exit()
    gs = GameSpace()
    endpoint = TCP4ClientEndpoint(reactor, sys.argv[1], sys.argv[2])
    d = point.connect(CommandFactory(gs))
    d.addCallback(gotProtocol)
    reactor.run()
