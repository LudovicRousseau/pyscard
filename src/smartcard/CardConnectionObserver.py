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

# pylint: disable=too-few-public-methods


# ReaderObserver interface
class CardConnectionObserver(Observer):
    """
    CardConnectionObserver is a base class for objects that are to be notified
    upon L{CardConnection} events.
    """

    def update(self, observable, arg):
        """Called upon CardConnection event.

        @param observable:         the observed card connection object
        @param arg:    the CardConnectionEvent sent by the connection
        """


class ConsoleCardConnectionObserver(CardConnectionObserver):
    """CardConnectionObserver output to the console"""

    def update(self, observable, arg):

        if "connect" == arg.type:
            print("connecting to " + observable.getReader())

        elif "reconnect" == arg.type:
            print("reconnecting to " + observable.getReader())

        elif "disconnect" == arg.type:
            print("disconnecting from " + observable.getReader())

        elif "release" == arg.type:
            print("release from " + observable.getReader())

        elif "command" == arg.type:
            print("> " + toHexString(arg.args[0]))

        elif "response" == arg.type:
            sw1, sw2 = arg.args[-2:]
            SW = f" {sw1:2X} {sw2:02X}"
            if [] == arg.args[0]:
                print("<  []" + SW)
            else:
                print("< " + toHexString(arg.args[0]) + SW)
        else:
            print("unknown event:", arg.type)
