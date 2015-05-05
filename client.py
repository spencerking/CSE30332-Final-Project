import sys
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
from game import GameSpace

class Client():
    def __init__(self, args):
        self.serverAddress = args[1]
        self.serverPort = args[2]
        self.gs = GameSpace(self, args[3])

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
        if data == 'POS':
            self.gs.initEnemy(data)
        elif data == 'MOVE':
            self.gs.enemy.key_handler(__keycode__)
        elif data == 'FIRE':
            self.gs.fire(self.gs.enemy)
        elif data == 'TURRET':
            self.gs.enemy.turret_direction = __turret_direction__

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: $ python client.py <address> <port> <tank type>'
        sys.exit()
    client = Client(sys.argv)
    client.run()
