"""Smartcard module exceptions.

This module defines the exceptions raised by the smartcard.pcsc modules.

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

# gemalto scard library
import smartcard.scard


class BaseSCardException(Exception):
    """Base class for scard (aka PCSC) exceptions.

    scard exceptions are raised by the scard module, i.e.
    low-level PCSC access to readers and cards.

    """

    def __init__(self, hresult):
        """Constructor that stores the pcsc error status."""
        self.hresult = hresult

    def __str__(self):
        """Returns a string representation of the exception."""
        return repr("scard exception: " +
            smartcard.scard.SCardGetErrorMessage(self.hresult))


class AddReaderToGroupException(BaseSCardException):
    """Raised when scard fails to add a new reader to a PCSC reader group."""

    def __init__(self, hresult, readername="", groupname=""):
        BaseSCardException.__init__(self, hresult)
        self.readername = readername
        self.groupname = groupname

    def __str__(self):
        return repr('Failure to add reader: ' + self.readername +
            ' to group: ' + self.groupname + ' ' +
            smartcard.scard.SCardGetErrorMessage(self.hresult))


class EstablishContextException(BaseSCardException):
    """Raised when scard failed to establish context with PCSC."""

    def __str__(self):
        """Returns a string representation of the exception."""
        return repr('Failure to establish context: ' +
            smartcard.scard.SCardGetErrorMessage(self.hresult))


class ListReadersException(BaseSCardException):
    """Raised when scard failed to list readers."""

    def __str__(self):
        return repr('Failure to list readers: ' +
            smartcard.scard.SCardGetErrorMessage(self.hresult))


class IntroduceReaderException(BaseSCardException):
    """Raised when scard fails to introduce a new reader to PCSC."""

    def __init__(self, hresult, readername=""):
        BaseSCardException.__init__(self, hresult)
        self.readername = readername

    def __str__(self):
        return repr('Failure to introduce a new reader: ' + self.readername
            + ' ' + smartcard.scard.SCardGetErrorMessage(self.hresult))


class ReleaseContextException(BaseSCardException):
    """Raised when scard failed to release PCSC context."""

    def __str__(self):
        return repr('Failure to release context: ' +
            smartcard.scard.SCardGetErrorMessage(self.hresult))


class RemoveReaderFromGroupException(BaseSCardException):
    """Raised when scard fails to remove a reader from a PCSC reader group."""

    def __init__(self, hresult, readername="", groupname=""):
        BaseSCardException.__init__(self, hresult)
        self.readername = readername
        self.groupname = groupname

    def __str__(self):
        return repr('Failure to remove reader: ' + self.readername +
            ' from group: ' + self.groupname + ' ' +
            smartcard.scard.SCardGetErrorMessage(self.hresult))

if __name__ == "__main__":
    try:
        raise EstablishContextException(smartcard.scard.SCARD_E_NO_MEMORY)
    except BaseSCardException as exc:
        print(exc)

