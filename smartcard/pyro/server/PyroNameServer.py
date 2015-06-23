"""Utility class to start/stop Pyro Name Server.

__author__ = "http://www.gemalto.com"

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
import signal
import sys
from threading import Thread
import time

import Pyro.naming
import Pyro.nsc
import Pyro.util


class PyroNameServer(Thread):
    """Thread running the Pyro Name server.
    """

    def __init__(self, args=[]):
        """Initialize pyro name server with command line arguments.
        For a complete list of command line arguments, see pyro documentation
        for pyro-ns start script."""
        Thread.__init__(self)
        self.setDaemon(True)
        self.setName('smartcard.pyro.server.PyroNameServer')
        self.args = args
        self.handler = signal.signal(signal.SIGINT, self)

        _args = []
        for arg in self.args:
            _args.append(arg)
        Args = Pyro.util.ArgParser()
        Args.parse(_args, 'hkmrvxn:p:b:c:d:s:i:1:2:')
        self.host = Args.getOpt('n', None)
        self.bcport = Args.getOpt('b', None)
        self.bcaddr = Args.getOpt('c', None)
        self.identification = Args.getOpt('i', None)

    def getShutdownArgs(self):
        """return command line arguments for shutting down the
        server; this command line is built from the name server
        startup arguments."""
        shutdownArgs = []
        if self.host:
            shutdownArgs += ['-h', self.host]
        if self.bcport:
            shutdownArgs += ['-p', self.bcport]
        if self.bcaddr:
            shutdownArgs += ['-c', self.bcaddr]
        if self.identification:
            shutdownArgs += ['-i', self.identification]

        return shutdownArgs

    def listall(self):
        """List pyro namespace."""
        args = self.getShutdownArgs() + ['listall']
        Pyro.nsc.main(args)

    def ping(self):
        """Ping pyro naming server."""
        args = self.getShutdownArgs() + ['ping']
        Pyro.nsc.main(args)

    def run(self):
        """Starts Pyro naming server with command line arguments
        (see pyro documentation)"""
        args = []
        for arg in self.args:
            args.append(arg)
        Pyro.naming.main(args)

    def stop(self):
        """Shutdown pyro naming server."""
        args = self.getShutdownArgs() + ['shutdown']
        Pyro.nsc.main(args)
        self.join()

    def waitStarted(self):
        """wait until name server is started."""
        ns = None
        while not ns:
            try:
                time.sleep(3)
                ns = Pyro.naming.NameServerLocator(
                    identification=self.identification).getNS()
            except Pyro.errors.NamingError as er:
                pass

    def __call__(self, signame, sf):
        """Ctrl+c handler that will gracefully shutdown the server
        upon Ctrl+C signal"""
        print('PyroNameServer Ctrl+C handler')
        self.stop()
        time.sleep(1)
        self.handler(signame, sf)


if __name__ == '__main__':
    import sys
    pt = PyroNameServer(sys.argv[1:])
    pt.start()
    pt.waitStarted()
    pt.stop()
