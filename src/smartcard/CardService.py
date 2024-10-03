"""Card service abstract class.

A card service is a class providings specific smart card functionality,
e.g.  a GSM file system or an Open Platform loader.  CardService is an
abstract class from which concrete card services are derived.  A concrete
card service is almost always smart card operating system specific.

The card service performs its specific smart card functionality by accessing
the smartcard with a CardConnection.

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

from smartcard.scard import *


class CardService:
    """Card service abstract class."""

    def __init__(self, connection, cardname=None):
        """Construct a new card service and bind to a smart card in a reader.

        @param connection:     the CardConnection used to access the smart card
        """
        self.connection = connection
        self.cardname = cardname

    def __del__(self):
        """Destructor. Disconnect card and destroy card service resources."""
        self.connection.disconnect()

    @staticmethod
    def supports(cardname):
        pass


if __name__ == "__main__":
    """Small sample illustrating the use of CardService."""
    SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    DF_TELECOM = [0x7F, 0x10]
    from smartcard.System import readers

    cc = readers()[0].createConnection()
    cs = CardService(cc)
    cs.connection.connect()
    data, sw1, sw2 = cs.connection.transmit(SELECT + DF_TELECOM)
    print(f"{sw1:X} {sw2:X}")
    cs.connection.disconnect()
