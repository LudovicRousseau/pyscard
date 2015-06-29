"""PyroReaderClient: concrete reader class for Remote Readers

__author__ = "gemalto http://www.gemalto.com"

Copyright 2001-2012 gemalto
Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com

This file is part of pyscard.

pyscard is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or
(at your option) any later version.

pyscard is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyscard; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

from __future__ import print_function
import Pyro.core
import Pyro.naming

from smartcard.Exceptions import NoCardException
from smartcard.reader.Reader import Reader


class PyroReader(Reader):
    """Remote reader class."""
    def __init__(self, readername):
        """Constructs a new Remote Reader client implementation from a
        Pyro URI."""
        ns = Pyro.naming.NameServerLocator().getNS()
        self.uri = ns.resolve(':pyscard.smartcard.readers.' + readername)
        self.reader = Pyro.core.getAttrProxyForURI(self.uri)
        self.name = self.reader.name

    def addtoreadergroup(self, groupname):
        """Add reader to a reader group."""
        self.reader.addtoreadergroup(groupname)

    def removefromreadergroup(self, groupname):
        """Remove a reader from a reader group"""
        self.reader.removefromreadergroup(groupname)

    def createConnection(self):
        """Return a card connection thru a remote reader."""
        uri = self.reader.createConnection()
        return Pyro.core.getAttrProxyForURI(uri)

    class Factory:
        def create(readername):
            return PyroReader(readername)
        create = staticmethod(create)

    def readers(groups=[]):
        readernames = []
        try:
            ns = Pyro.naming.NameServerLocator().getNS()
            readernames = ns.list(':pyscard.smartcard.readers')
        except Pyro.errors.NamingError:
            print('Warning: pyro name server not found')

        remotereaders = []
        for readername in readernames:
            remotereaders.append(PyroReader.Factory.create(readername[0]))

        return remotereaders
    readers = staticmethod(readers)

if __name__ == '__main__':
    SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    DF_TELECOM = [0x7F, 0x10]
    from smartcard.util import *

    remotereaders = PyroReader.readers()
    for reader in remotereaders:
        try:
            print(reader.name, ', uri: ', reader.uri)
            connection = reader.createConnection()
            connection.connect()
            print(toHexString(connection.getATR()))
            data, sw1, sw2 = connection.transmit(SELECT + DF_TELECOM)
            print("%X %X" % (sw1, sw2))
        except NoCardException as x:
            print('no card in reader')
