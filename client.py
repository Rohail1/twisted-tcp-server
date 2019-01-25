from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):

    def connectionMade(self):
        self.sendQuote()

    def sendQuote(self):
        self.transport.write(self.factory.quote)

    def dataReceived(self, data):
        print('server responded :', data)
        self.transport.loseConnection()


class EchoFactory(protocol.ClientFactory):

    protocol = EchoClient

    def __init__(self, quote):
            self.quote = quote

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.", reason.getErrorMessage())
        maybe_stop_reactor()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.", reason.getErrorMessage())
        maybe_stop_reactor()


def maybe_stop_reactor():
    global quote_counter
    quote_counter -= 1
    if not quote_counter:
        reactor.stop()


quotes = [
    b"You snooze you lose",
    b"The early bird gets the worm",
    b"Carpe diem"
]
quote_counter = len(quotes)

for quote in quotes:
    reactor.connectTCP('localhost', 8000, EchoFactory(quote))
reactor.run()