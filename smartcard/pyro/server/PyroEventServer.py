"""Utility class to start/stop Pyro Event Server.

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

import Pyro.EventService.Server
import Pyro.naming
import Pyro.nsc
import Pyro.util


class PyroEventServer(Thread):
    """Thread running the Pyro Event server.
    """

    def __init__(self, args=[]):
        """Initialize pyro event server with command line arguments.
        For a complete list of command line arguments, see pyro documentation
        for pyro-es start script."""
        Thread.__init__(self)
        self.setDaemon(True)
        self.setName('smartcard.pyro.server.PyroEventServer')
        self.args = args
        self.handler = signal.signal(signal.SIGINT, self)
        self.starter = None

    def run(self):
        """Starts Pyro naming server with command line arguments (see
        pyro documentation) """
        args = []
        for arg in self.args:
            args.append(arg)
        Args = Pyro.util.ArgParser()
        Args.parse(args, 'hkmrvxn:p:b:c:d:s:i:1:2:')

        hostname = Args.getOpt('n', None)
        identification = Args.getOpt('i', None)
        port = None
        useNameServer = True

        if port:
            port = int(port)
        norange = (port == 0)

        self.starter = Pyro.EventService.Server.EventServiceStarter(
            identification=identification)
        self.starter.start(
            hostname, port, useNameServer=useNameServer, norange=norange)

    def stop(self):
        """Shutdown pyro event server."""
        pass

    def waitStarted(self):
        """wait until name server is started."""
        started = False
        while not started:
            if self.starter != None:
                started = self.starter.waitUntilStarted(0.5)

    def __call__(self, signame, sf):
        """Ctrl+c handler that will gracefully shutdown the server
        upon Ctrl+C signal"""
        print('PyroEventServer Ctrl+C handler')
        self.stop()
        time.sleep(1)
        self.handler(signame, sf)


if __name__ == '__main__':
    from smartcard.pyro.server.PyroNameServer import PyroNameServer
    pn = PyroNameServer(sys.argv[1:])
    pn.start()
    pn.waitStarted()
    pe = PyroEventServer(sys.argv[1:])
    pe.start()
    pe.waitStarted()
    pn.listall()
    pe.stop()
    pn.stop()
