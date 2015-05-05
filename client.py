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
    def connectionMade(self):


    def dataReceived(self, data):


if __name__ == '__main__':
    client = Client(sys.argv)
    client.run()
