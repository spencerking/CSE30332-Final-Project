import sys
from random import randint
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet import reactor

class Map():
    def __init__(self):
        # Generate map tiles so both clients present the same map
        self.map = []
        self.map_height = self.map_width = 7
        for i in range(0, self.map_height):
            self.map.append([])
            for j in range(0, self.map_width):
                self.map[i].append(randint(0,2))
        self.player_positions = {}
        self.player_types = {}

    def getValidStartPos(self, name):
        rowPos = randint(0, self.map_height-1)
        row = self.map[rowPos]
        tile = row[randint(0, self.map_width-1)]
        while 1:
            for player, position in self.player_positions:
                if tile != 2 and (rowPos, tile) != position:
                    self.player_positions[name] = (rowPos, tile)
                    return (rowPos, tile)
            rowPos = randint(0, self.map_height-1)
            row = self.map[rowPos]
            tile = row[randint(0, self.map_width-1)]    

class Command(LineReceiver):
    def __init__(self, factory, num):
        self.players = factory.players
        self.id = num
        self.MAP = factory.map
        self.name = None
        self.type = None
        self.state = 'GETNAME'

    def connectionMade(self):
        print 'Client %d connected' % self.id
        # Give the client the map size and tile list
        map_str = ''
        for i, row in enumerate(self.MAP.map):
            for j, item in enumerate(row):
                map_str += str(item)+','
        map_str = map_str[0:len(map_str)-1]
        size_str = str(self.MAP.map_width) +','+ str(self.MAP.map_height)
        self.sendLine('MAP,' + size_str +','+ map_str)

        # Give the client a start position
        pos = self.MAP.getValidStartPos(self.name)
        self.sendLine('POS1,' + str(pos[0]) +','+ str(pos[1]))

        self.sendLine('What\'s your name?')

    def connectionLost(self, reason):
        for name, protocol in self.players.iteritems():
            if protocol != self:
                protocol.sendLine('QUIT,' + name)
        if self.map.player_positions.has_key(self.name):
            del self.map.player_positions[self.name]
        if self.map.player_types.has_key(self.name):
            del self.map.player_types[self.name]
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
        self.sendLine('Please choose your tank:\ngreen, blue, red')

    def handleGETTANKTYPE(self, tank):
        if tank in ['green', 'blue', 'red']:
            self.type = tank
            self.sendLine('TYPE,' + tank)
        else:
            self.sendLine('Unknown type, please choose another:')
            return
        self.state = 'WAITFOROPPONENT'

    def handle_WAITFOROPPONENT(self):
        for name, protocol in self.players.iteritems():
            if protocol != self:
                if protocol.state == 'WAITFOROPPONENT':
                    # Send our name and tank type to other player(s)
                    protocol.sendLine('POS2,' + self.name +','+ self.type +','+ str(self.map.player_positions[self.name][0]) +','+ str(self.map.player_positions[self.name][1]))
                else:
                    return
        self.state = 'FIGHT'

    def handle_FIGHT(self, line):
        for name, protocol in self.players.iteritems():
            if protocol != self:
                protocol.sendLine(line)

class CommandFactory(Factory):
    def __init__(self, MAP):
        self.players = {}
        self.map = MAP

    def buildProtocol(self, addr):
        return Command(self, len(self.players))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: $ python server.py <port>'
        sys.exit()
    MAP = Map()
    reactor.listenTCP(int(sys.argv[1]), CommandFactory(MAP))
    reactor.run()
