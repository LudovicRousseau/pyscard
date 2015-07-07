"""RemoteReaderServer: monitor local readers and publish them as pyro
Remote Readers.

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

try:
    import Pyro.core
    import Pyro.naming
except ImportError:
    print('You need pyro (python remote objects) ' + \
          'at http://www.xs4all.nl/~irmen/pyro3/')
    import sys
    sys.exit()

from smartcard.reader.Reader import Reader
from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver
from smartcard.pyro.server.RemoteCardConnection import RemoteCardConnection
from smartcard.pyro.server import PyroDaemon
from smartcard.pyro.server import PyroNameServer


class RemoteReader(Reader, Pyro.core.ObjBase):
    """Remote reader class that embeds a local reader."""

    def __init__(self, reader):
        """Encapsulate a local reader and publish as a pyro remote reader.

        reader: the local reader to publish remotely
        """
        Pyro.core.ObjBase.__init__(self)
        self.readerobj = reader
        self.name = reader.name

    def addtoreadergroup(self, groupname):
        """Add reader to a reader group."""
        self.readerobj.reader.addtoreadergroup(groupname)

    def removefromreadergroup(self, groupname):
        """Remove a reader from a reader group"""
        self.readerobj.reader.removefromreadergroup(groupname)

    def createConnection(self):
        """Return a card connection thru the reader."""
        connection = RemoteCardConnection(self.readerobj.createConnection())
        daemon = PyroDaemon.PyroDaemon()
        uri = daemon.connect(connection)
        return uri


class RemoteReaderServer(ReaderObserver):
    """Monitor local readers, and publish them as remote pyro readers.
    """
    def __init__(self):
        """Starts pyro name server and constructs reader name space."""
        self.pn = PyroNameServer.PyroNameServer()
        self.pn.start()
        self.pn.waitStarted()

        Pyro.core.initServer()
        self.ns = Pyro.naming.NameServerLocator().getNS()
        try:
            self.ns.createGroup(':pyscard')
            self.ns.createGroup(':pyscard.smartcard')
            self.ns.createGroup(':pyscard.smartcard.readers')
        except Pyro.errors.NamingError as error:
            print(error)
        self.daemon = PyroDaemon.PyroDaemon()
        self.remotereaders = {}

    def start(self):
        """Start pyro daemon and accept incoming requests."""
        self.daemon.start()

    def update(self, observable, actions):
        """Called when a local reader is added or removed.
        Create remote pyro reader objects for added readers.
        Delete remote pyro reader objects for removed readers."""
        (addedreaders, removedreaders) = actions
        for reader in addedreaders:
            remotereader = RemoteReader(reader)
            self.remotereaders[reader.name] = remotereader
            name = "".join(reader.name.split(' '))
            name = ":pyscard.smartcard.readers." + "".join(name.split('.'))
            uri = self.daemon.connect(remotereader, name)
        for reader in removedreaders:
            remotereader = self.remotereaders[reader.name]
            self.daemon.disconnect(remotereader)
            del self.remotereaders[reader.name]
        self.pn.listall()


if __name__ == '__main__':
    readerserver = RemoteReaderServer()
    readermonitor = ReaderMonitor()
    readermonitor.addObserver(readerserver)
    print('Reader remote server up and running', end=' ')
    print('Please enter Ctrl+C to stop and exit...')
    readerserver.start()
