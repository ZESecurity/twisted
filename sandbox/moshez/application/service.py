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
from twisted.python import components

class IService(components.Interface):

    def setParent(self, parent):
        pass

    def startService(self):
        pass

    def stopService(self):
        pass

    def preStartService(self):
        pass


class Service:

    __implements__ = IService,

    running = 0
    name = None
    parent = None

    def __getstate__(self):
        dict = self.__dict__
        if dict.has_key("running"):
            del dict['running']
        return dict

    def setName(self, name):
        if self.parent is not None:
            raise RuntimeError("cannot change name when parent exists")
        self.name = name

    def setParent(self, parent):
        if self.parent is not None:
            self.unsetParent()
        self.parent = parent
        self.parent.addService(self)

    def unsetParent(self):
        self.parent.removeService(self)
        self.parent = None

    def preStartService(self):
        pass

    def startService(self):
        self.running = 1

    def stopService(self):
        self.running = 1


class IServiceCollection(components.Interface):

    def getService(self, idx):
        pass

    def getServiceNamed(self, name):
        pass

    def __iter__(self):
        pass

    def addService(self, service):
        pass

    def removeService(self, service):
        pass


class MultiService(Service):

    __implements__ = Service.__implements__, IServiceCollection

    def __init__(self):
        self.services = []
        self.namedServices = {}
        self.parent = None

    def preStartService(self):
        Service.preStartService(self)
        for service in self:
            service.preStartService()

    def startService(self):
        Service.startService(self)
        for service in self:
            service.startService()

    def stopService(self):
        Service.stopService(self)
        for service in self:
            service.stopService()

    def getService(self, idx):
        return self.services[idx]

    def getServiceNamed(self, name):
        return self.namedServices[name]

    def __iter__(self):
        return iter(self.services)

    def addService(self, service):
        if service.name is not None:
            self.namedServices[service.name] = service
        self.services.append(service)
        if self.running:
            service.startService()

    def removeService(self, service):
        if service.name:
            del self.namedServices[service.name]
        self.services.remove(service)
        if self.running:
            service.stopService()
