import sys
from random import randint
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Map():
    def __init__(self):
        # Generate map tiles so both clients generate the same map
        self.map = []
        self.map_height = self.map_width = 7
        for i in range(0, self.map_height):
            self.map.append([])
            for j in range(0, self.map_width):
                self.map[i].append(randint(0,2))
        self.player_pos = {}
        self.player_types = {}

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

class Command(LineReceiver):
    def __init__(self, factory):
        self.players = factory.players
        self.map = factory.map
        self.name = None
        self.type = None
        self.state = 'GETNAME'

    def connectionMade(self):
        # Give the client the map size and tile list
        map_str = ''
        for i, row in enumerate(self.map):
            for j, item in enumerate(row):
                map_str += str(item)+','
        map_str = map_str[0:len(map_str)-1]
        size_str = str(self.map_width) +','+ str(self.map_height)
        self.sendLine('MAP,' + size_str +','+ map_str)

        # Give the client a start position
        pos = self.map.getValidStartPos()
        self.transport.write('POS,' + str(pos[0]) +','+ str(pos[1]) + '\r\n')

        self.sendLine('What\'s your name?')

    def connectionLost(self, reason):
        for name, protocol in self.players.iteritems():
            if protocol != self:
                protocol.sendLine('QUIT,' + name)
        if self.players.has_key(self.name):
            del self.players[self.name]

    def lineReceived(self, line):
        if self.state == 'GETNAME':
            self.handle_GETNAME(line)
        elif self.state == 'GETTANKTYPE':
            self.handle_GETTANKTYPE(line)
        elif self.state == 'WAITFOROPPONENT':
            self.handle_WAITFOROPPONENT()
        elif self.state == 'FIGHT':
            self.handle_FIGHT(line)

    def handle_GETNAME(self, name):
        if self.players.has_key(name):
            self.sendLine('Name taken, please choose another:')
            return
        self.name = name
        self.players[name] = self
        self.state = 'GETTANKTYPE'
        self.sendLine('Please choose your tank:\nGreen, blue, red')

    def handleGETTANKTYPE(self, tank):
        if tank == 'green':
            self.type = 'green'
        elif tank == 'blue':
            self.type = 'blue'
        elif tank == 'red':
            self.type = 'red'
        else:
            self.sendLine('Unknown type, please choose another:')
            return
        self.state = 'WAITFOROPPONENT'

    def handle_WAITFOROPPONENT(self):
        while len(self.players) < 2:
            pass
        for name, protocol in self.players.iteritems():
            if protocol != self:
                protocol.sendLine('TYPE,' + name +','+ protocol.type)

    def handle_FIGHT(self, line):
        for name, protocol in self.players.iteritems():
            if protocol != self:
                protocol.sendLine(line)

class CommandFactory(Factory):
    def __init__(self, MAP):
        self.players = {}
        self.map = MAP

    def buildProtocol(self, addr):
        return Command(self)

if __name__ == '__main__':
    MAP = Map()
    reactor.listenTCP(9900, CommandFactory(MAP))
    reactor.run()
