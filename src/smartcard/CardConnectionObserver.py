"""CardConnectionObserver interface.

CardConnectionObserver is a base class for objects that are to be notified
upon CardConnection events.

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

from smartcard.Observer import Observer
from smartcard.util import toHexString


# ReaderObserver interface
class CardConnectionObserver(Observer):
    """
    CardConnectionObserver is a base class for objects that are to be notified
    upon L{CardConnection} events.
    """

    def update(self, cardconnection, cardconnectionevent):
        """Called upon CardConnection event.

        @param cardconnection:         the observed card connection object
        @param cardconnectionevent:    the CardConnectionEvent sent by the connection
        """
        pass


class ConsoleCardConnectionObserver(CardConnectionObserver):

    def update(self, cardconnection, ccevent):

        if "connect" == ccevent.type:
            print("connecting to " + cardconnection.getReader())

        elif "reconnect" == ccevent.type:
            print("reconnecting to " + cardconnection.getReader())

        elif "disconnect" == ccevent.type:
            print("disconnecting from " + cardconnection.getReader())

        elif "release" == ccevent.type:
            print("release from " + cardconnection.getReader())

        elif "command" == ccevent.type:
            print("> " + toHexString(ccevent.args[0]))

        elif "response" == ccevent.type:
            if [] == ccevent.args[0]:
                print("<  [] %02X %02X" % tuple(ccevent.args[-2:]))
            else:
                print(
                    "< "
                    + toHexString(ccevent.args[0])
                    + " "
                    + "%02X %02X" % tuple(ccevent.args[-2:])
                )
        else:
            print("unknown event:", ccevent.type)
