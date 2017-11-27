"""Card service abstract class.

A card service is a class providings specific smart card functionality,
e.g.  a GSM file system or an Open Platform loader.  CardService is an
abstract class from which concrete card services are derived.  A concrete
card service is almost always smart card operating system specific

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
from smartcard import CardService


class PassThruCardService(CardService.CardService):
    """Pass-thru card service class."""

    def __init__(self, connection, cardname=None):
        """Construct a pass-thru card service.

        connection:     the CardConnection used to access the smart card
        """
        CardService.CardService.__init__(self, connection, cardname)

    def supports(cardname):
        """Returns True if the cardname is supported by the card service.
        The PassThruCardService supports all cardnames and always
        returns True."""
        return True

    supports = staticmethod(supports)

if __name__ == '__main__':
    """Small sample illustrating the use of CardService."""
    SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    DF_TELECOM = [0x7F, 0x10]
    from smartcard.System import readers
    cc = readers()[0].createConnection()
    cs = PassThruCardService(cc)
    cs.connection.connect()
    data, sw1, sw2 = cs.connection.transmit(SELECT + DF_TELECOM)
    print("%X %X" % (sw1, sw2))
    cs.connection.disconnect()
