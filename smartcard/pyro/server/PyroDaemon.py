"""PyroDaemon: Wrapper class around pyro daemon

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
import signal
from threading import Thread
import time

import Pyro.core
import Pyro.naming


class PyroDaemon(object):
    """Singleton class to wrap the pyro daemon."""

    class _PyroDaemon:
        """The pyro daemon actual wrapper class.

        A single instance of this class is created
        by the public PyroDaemon class.
        """
        def __init__(self):
            self.daemon = Pyro.core.Daemon()
            self.handler = signal.signal(signal.SIGINT, self)
            ns = Pyro.naming.NameServerLocator().getNS()
            self.daemon.useNameServer(ns)

        def __call__(self, signame, sf):
            """Ctrl+c handler that will gracefully shutdown the server
            upon Ctrl+C signal"""
            print('PyroDaemon Ctrl+C handler')
            self.daemon.shutdown(True)
            time.sleep(1)
            self.handler(signame, sf)

        def connect(self, object, name=None):
            return self.daemon.connect(object, name)

        def disconnect(self, object):
            return self.daemon.disconnect(object)

        def start(self):
            """start pyro daemon."""
            self.daemon.requestLoop()

    # the singleton
    instance = None

    def __init__(self):
        if not PyroDaemon.instance:
            PyroDaemon.instance = PyroDaemon._PyroDaemon()

    def __getattr__(self, name):
        return getattr(self.instance, name)


class PyroDaemonThread(Thread):
    """Thread running the Pyro daemon server.
    """

    def __init__(self):
        """Initialize pyro event server with command line arguments.
        For a complete list of command line arguments, see pyro documentation
        for pyro-es start script."""
        Thread.__init__(self)
        self.setDaemon(True)
        self.setName('smartcard.pyro.server.PyroDaemonThread')
        self.daemon = PyroDaemon()

    def run(self):
        """Starts Pyro daemon."""
        self.daemon.start()
