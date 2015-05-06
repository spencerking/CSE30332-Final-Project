import sys
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
        self.occupied_pos = []

    def getValidStartPos(self):
        row = self.map[randint(0, self.map_height)]
        tile = row[randint(0, self.map_width)]
        while tile == 2 and (row, tile) not in self.occupied_pos:
            row = self.map[randint(0, self.map_height)]
            tile = row[randint(0, self.map_width)]
        self.occupied_pos.append((row, tile))
        return (row, tile)
        
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
        self.server = factory.server
        self.conn_id = conn_id

    def connectionMade(self):
        print 'Client %d joined' % self.conn_id
        # Give the client the tile list
        map_str = ''
        for i in self.server.map:
            for j in self.server.map[i]:
                map_str += str(j)+','
        map_str = map_str[1:len(map_str)-1]
        size_str = str(self.server.map_width) +','+ str(self.server.map_height)
        self.transport.write('MAP,' + size_str +','+ map_str)
        # Give the client a start position
        pos = self.server.getValidStartPos()
        self.transport.write('POS1,' + str(pos[0]) +','+ str(pos[1]))

    def connectionLost(self):
        print 'Client %d left' % self.conn_id
        # Tell other client that this client left
        self.server.connections[self.conn_id-1].transport.write('QUIT')

        # TODO: Quit cleanly

    def dataReceived(self, data):
        # Get data from client and send it to other client
        self.server.connections[self.conn_id-1].transport.write(data)
    
if __name__ == '__main__':
    server = Server(sys.argv)
    server.run()
