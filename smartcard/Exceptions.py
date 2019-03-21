"""Smartcard module exceptions.

This module defines the exceptions raised by the smartcard module.

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

from smartcard.scard import SCardGetErrorMessage


class SmartcardException(Exception):
    """Base class for smartcard exceptions.

    smartcard exceptions are generated by the smartcard module and
    shield scard (i.e. PCSC) exceptions raised by the scard module.

    """
    def __init__(self, message="", hresult=-1, *args):
        super(SmartcardException, self).__init__(message, *args)
        self.hresult = int(hresult)

    def __str__(self):
        text = super(SmartcardException, self).__str__()
        if self.hresult != -1:
            text += ": %s (0x%08X)" % (SCardGetErrorMessage(self.hresult), self.hresult)

        return text



class CardConnectionException(SmartcardException):
    """Raised when a CardConnection class method fails."""
    pass


class CardRequestException(SmartcardException):
    """Raised when a CardRequest wait fails."""
    pass


class CardRequestTimeoutException(SmartcardException):
    """Raised when a CardRequest times out."""

    def __init__(self, *args):
        SmartcardException.__init__(self,
                                    "Time-out during card request", *args)


class CardServiceException(SmartcardException):
    """Raised when a CardService class method fails."""
    pass


class CardServiceStoppedException(SmartcardException):
    """Raised when a CardService was stopped"""
    pass


class InvalidATRMaskLengthException(SmartcardException):
    """Raised when an ATR mask does not match an ATR length."""

    def __init__(self, mask):
        SmartcardException.__init__(self, 'Invalid ATR mask length: %s'
            %mask)


class InvalidReaderException(SmartcardException):
    """Raised when trying to acces an invalid smartcard reader."""

    def __init__(self, readername):
        SmartcardException.__init__(self, 'Invalid reader: %s' % readername)


class ListReadersException(SmartcardException):
    """Raised when smartcard readers cannot be listed."""

    def __init__(self, hresult):
        SmartcardException.__init__(self, 'Failed to list readers',
                hresult=hresult)


class NoCardException(SmartcardException):
    """Raised when no card in is present in reader."""

    def __init__(self, message, hresult):
        SmartcardException.__init__(self, message, hresult=hresult)


class NoReadersException(SmartcardException):
    """Raised when the system has no smartcard reader."""

    def __init__(self, *args):
        SmartcardException.__init__(self, 'No reader found', *args)
