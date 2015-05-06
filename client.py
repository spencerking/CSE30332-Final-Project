import sys
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from game import GameSpace

class Client():
    def __init__(self, args):
        self.serverAddress = args[1]
        self.serverPort = args[2]
        self.gs = GameSpace(self, args[2], args[3])

    def run(self):
        gameLoop = LoopingCall(gs.main)
        gameLoop.start(1.0/60)
        factory = ClientConnFactory()
        reactor.connectTCP(self.serverAddress, self.serverPort, factory)
        reactor.run()

class ClientConnFactory(ClientFactory):
    def buildProtocol(self, addr):
        return CommandConnProtocol()

class ClientConnProtocol(Protocol):
    def dataReceived(self, data):
        data = data.rstrip()
        tokens = data.split(',')
        if tokens[0] == 'POS':
            #                 tankType,  (position)
            self.gs.initEnemy(tokens[1], (tokens[2], tokens[3]))
        elif tokens[0] == 'MOV':
            #                         keycode
            self.gs.enemy.key_handler(tokens[1])
        elif tokens[0] == 'FIR':
            self.gs.fire(self.gs.enemy)
        elif tokens[0] == 'TUR':
            #                                turret direction
            self.gs.enemy.turret_direction = tokens[1]

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: $ python client.py <address> <port> <tank type>'
        print 'Tank types are "blue", "green", and "red"'
        sys.exit()
    client = Client(sys.argv)
    client.run()
