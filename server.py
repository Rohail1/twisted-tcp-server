from twisted.internet import protocol, reactor


class Echo(protocol.Protocol):

    def dataReceived(self, data):
        print("Number of active connections %s" % self.factory.numberOfConnections)
        print("Quote from client %s" % self.getQuote())
        self.transport.write(self.getQuote())
        self.updateQuote(data)

    def connectionMade(self):
        print("Connection Details %s" % self.transport.getPeer())
        self.factory.numberOfConnections += 1

    def connectionLost(self, reason):
        self.factory.numberOfConnections -= 1

    def getQuote(self):
        return self.factory.quote

    def updateQuote(self, data):
        self.factory.quote = data


class EchoFactory(protocol.Factory):

    numberOfConnections = 0
    protocol = Echo

    def __init__(self, quote=None):
        self.quote = quote or b"An apple a day keeps the doctor away"

    def doStart(self):
        print('Server listening at 8000')


reactor.listenTCP(8000, EchoFactory())
reactor.run()
