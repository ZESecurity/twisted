from twisted.python.log import startLogging
from sys import stdout
startLogging(stdout)

# # cut here

from twisted.tubes.protocol import factoryFromFlow
from twisted.internet.endpoints import serverFromString
from twisted.internet.defer import Deferred
from twisted.tubes.tube import Tube, series

class Reverser(Tube):
    def received(self, item):
        yield b"".join(reversed(item))

def reverseFlow(fount, drain):
    from twisted.tubes.framing import bytesToLines, linesToBytes
    lineReverser = series(bytesToLines(), Reverser(), linesToBytes())
    fount.flowTo(lineReverser).flowTo(drain)

def main(reactor, listenOn="stdio:"):
    endpoint = serverFromString(reactor, listenOn)
    endpoint.listen(factoryFromFlow(reverseFlow))
    return Deferred()

from twisted.internet.task import react

from sys import argv
react(main, argv[1:])
