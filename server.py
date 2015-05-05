from rand import randint
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from game import GameSpace

class Server():
    def __init__(self):
        self.port1 = 9900
        self.port2 = 9901
        self.connections = []
        
    def run(self):
        factory = ClientConnFactory(self)
        reactor.listenTCP(self.port1, factory)
        reactor.listenTCP(self.port2, factory)
        reactor.run()

class ClientConnFactory(Factory):
    def __init__(self, server):
        self.server = server

    def buildProtocol(self, addr):
        newConn = ClientConnProtocol(self)
        self.server.connections.append(newConn)
        return newConn

class ClientConnProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):


    def connectionLost(self, reason):
        self.factory.server.connections

    def dataReceived(self, data):

    
if __name__ == '__main__':
    server = Server()
    server.run()
