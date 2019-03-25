"""PCSC context singleton.

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

from threading import RLock

from smartcard.scard import *
from smartcard.pcsc.PCSCExceptions import EstablishContextException


class PCSCContext(object):
    """Manage a singleton pcsc context handle."""

    class __PCSCContextSingleton:
        """The actual pcsc context class as a singleton."""

        def __init__(self):
            hresult, self.hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
            if hresult != 0:
                raise EstablishContextException(hresult)

        def getContext(self):
            return self.hcontext

        def releaseContext(self):
            return SCardReleaseContext(self.hcontext)

    # the singleton
    mutex = RLock()
    instance = None

    def __init__(self):
        PCSCContext.mutex.acquire()
        try:
            if not PCSCContext.instance:
                self.renewContext()
        finally:
            PCSCContext.mutex.release()

    def __getattr__(self, name):
        if self.instance:
            return getattr(self.instance, name)

    def renewContext():
        PCSCContext.mutex.acquire()
        try:
            if PCSCContext.instance is not None:
                PCSCContext.instance.releaseContext()

            PCSCContext.instance = PCSCContext.__PCSCContextSingleton()
        finally:
            PCSCContext.mutex.release()

        return PCSCContext.instance.getContext()
    renewContext = staticmethod(renewContext)
