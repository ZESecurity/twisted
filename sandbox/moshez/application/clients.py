# Twisted, the Framework of Your Internet
# Copyright (C) 2001-2003 Matthew W. Lefkowitz
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
from twisted.application import service

class _AbstractClient(service.Service):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __getstate__(self):
        d = service.Service.__getstate__(self)
        if d.has_key('_connection'):
            del d['_connection']
        return d

    def startService(self):
        service.Service.startService(self)
        self._connection = self.getConnection()

    def stopService(self):
        service.Service.stopService(self)
        #self._connection.stopConnecting()

    def getConnection(self):
        from twisted.internet import reactor
        return getattr(reactor, self.method)(*self.args, **self.kwargs)


class GenericClient(_AbstractClient):
    method = 'connectWith'

class TCPClient(_AbstractClient):
    method = 'connectTCP'

class UNIXClient(_AbstractClient):
    method = 'connectUNIX'

class SSLClient(_AbstractClient):
    method = 'connectSSL'

class UDPClient(_AbstractClient):
    method = 'connectUDP'

class UNIXDatagramClient(_AbstractClient):
    method = 'connectUNIXDatagram'

class MulticastClient(_AbstractClient):
    method = 'connectMulticast'
