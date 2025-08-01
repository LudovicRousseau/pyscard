"""Smartcard module exceptions.

This module defines the exceptions raised by the smartcard module.

__author__ = "https://www.gemalto.com/"

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

    def __init__(self, *args, message="", hresult=-1):
        if not message and len(args) > 0:
            message = args[0]
            args = args[1:]
        if -1 == hresult and len(args) > 0:
            hresult = args[0]
            args = args[1:]
        super().__init__(message, *args)
        self.hresult = int(hresult)

    def __str__(self):
        text = super().__str__()
        if self.hresult != -1:
            if text:
                text += ": "
            hresult = self.hresult
            if hresult < 0:
                # convert 0x-7FEFFFE3 into 0x8010001D
                hresult += 0x100000000
            text += f"{SCardGetErrorMessage(self.hresult)} (0x{hresult:08X})"

        return text


class CardConnectionException(SmartcardException):
    """Raised when a CardConnection class method fails."""


class CardRequestException(SmartcardException):
    """Raised when a CardRequest wait fails."""


class CardRequestTimeoutException(SmartcardException):
    """Raised when a CardRequest times out."""

    def __init__(self, *args, hresult=-1):
        if -1 == hresult and len(args) > 0:
            hresult = args[0]
            args = args[1:]
        SmartcardException.__init__(
            self, "Time-out during card request", hresult=hresult, *args
        )


class CardServiceException(SmartcardException):
    """Raised when a CardService class method fails."""


class CardServiceStoppedException(SmartcardException):
    """Raised when the CardService was stopped"""


class CardServiceNotFoundException(SmartcardException):
    """Raised when the CardService is not found"""


class InvalidATRMaskLengthException(SmartcardException):
    """Raised when an ATR mask does not match an ATR length."""

    def __init__(self, mask):
        SmartcardException.__init__(self, f"Invalid ATR mask length: {mask}")


class InvalidReaderException(SmartcardException):
    """Raised when trying to access an invalid smartcard reader."""

    def __init__(self, readername):
        SmartcardException.__init__(self, f"Invalid reader: {readername}")


class ListReadersException(SmartcardException):
    """Raised when smartcard readers cannot be listed."""

    def __init__(self, hresult):
        SmartcardException.__init__(self, "Failed to list readers", hresult=hresult)


class NoCardException(SmartcardException):
    """Raised when no card in is present in reader."""

    def __init__(self, message, hresult):
        SmartcardException.__init__(self, message, hresult=hresult)


class NoReadersException(SmartcardException):
    """Raised when the system has no smartcard reader."""

    def __init__(self, *args):
        SmartcardException.__init__(self, "No reader found", *args)
