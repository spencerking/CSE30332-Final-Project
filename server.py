from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

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
        newConn = ClientConnProtocol(self, len(self.server.connections)+1)
        self.server.connections.append(newConn)
        return newConn

class ClientConnProtocol(Protocol):
    def __init__(self, factory, conn_id):
        self.factory = factory
        self.conn_id = conn_id

    def dataReceived(self, data):
        # Get data from client and send it to other client
        self.factory.server.connections[self.conn_id-1].transport.write(data)
    
if __name__ == '__main__':
    server = Server()
    server.run()
