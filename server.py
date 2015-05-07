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
        self.player1_pos = None
        self.player1_type = None

    def getValidStartPos(self):
        rowPos = randint(0, self.map_height-1)
        row = self.map[rowPos]
        tile = row[randint(0, self.map_width-1)]
        while tile == 2 and (row, tile) not in self.occupied_pos:
            rowPos = randint(0, self.map_height-1)
            row = self.map[rowPos]
            tile = row[randint(0, self.map_width-1)]
        self.occupied_pos.append((rowPos, tile))
        return (rowPos, tile)
        
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
        for i, row in enumerate(self.server.map):
            for j, item in enumerate(row):
                map_str += str(item)+','
        map_str = map_str[0:len(map_str)-1]
        size_str = str(self.server.map_width) +','+ str(self.server.map_height)
        self.transport.write('MAP,' + size_str +','+ map_str + '\r\n')
        # Give the client a start position
        pos = self.server.getValidStartPos()
        self.transport.write('POS1,' + str(pos[0]) +','+ str(pos[1]) + '\r\n')

        if len(self.server.connections) == 1:
            self.server.player1_pos = pos
        elif len(self.server.connections) == 2:
            self.transport.write('POS2,' + str(self.server.player1_type) +','+ str(self.server.player1_pos[0]) +','+ str(self.server.player1_pos[1]) + '\r\n')

    def connectionLost(self, reason):
        print 'Client %d left' % self.conn_id
        # Tell other client that this client left
        if len(self.server.connections) > 1:
            self.server.connections[self.conn_id-1].transport.write('QUIT')
        self.server.connections.remove(self)

    def dataReceived(self, data):
        # Get player 1's type and save it
        data = data.rstrip()
        tokens = data.split(',')
        if tokens[0] == 'TYPE' and len(self.server.connections) == 1:
            self.server.player1_type = tokens[1]
        # Get data from client and send it to other client
        else:
            self.server.connections[self.conn_id-1].transport.write(data)
    
if __name__ == '__main__':
    server = Server(sys.argv)
    server.run()
