from random import randint
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

class Server():
    def __init__(self, args):
        self.port1 = 9900
        self.port2 = 9901
        self.connections = []

        # Generate map tiles so both clients generate the same map
        self.map_height = self.map_width = 7
        self.map = []
        for i in range(0, self.map_height):
            self.map.append([])
            for j in range(0, self.map_width):
                self.map[i].append(randint(0,2))

    def getValidStartPos(self):

        
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

    def connectionMade(self):
        print 'Client %d joined' % self.conn_id
        # Give the client the tile list
        map_str = ''
        for i in self.factory.server.map:
            for j in self.factory.server.map[i]:
                map_str += str(j)+','
        map_str = map_str[1:len(map_str)-1]
        window_str = str(self.factory.server.map_width) +','+ str(self.factory.server.map_height)
        self.transport.write('MAP,' + window_str +','+ map_str)
        # Give the client a start position
        pos = self.factory.server.getValidStartPos()
        self.transport.write('POS1,' + str(pos[0]) +','+ str(pos[1]))

    def connectionLost(self):
        print 'Client %d left' % self.conn_id
        # TODO: Quit cleanly

    def dataReceived(self, data):
        # Get data from client and send it to other client
        self.factory.server.connections[self.conn_id-1].transport.write(data)
    
if __name__ == '__main__':
    server = Server(sys.argv)
    server.run()
