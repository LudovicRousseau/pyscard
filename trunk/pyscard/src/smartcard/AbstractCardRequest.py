"""AbstractCardRequest class.

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

from smartcard.CardType import AnyCardType
from smartcard.PassThruCardService import PassThruCardService
import smartcard.System


class AbstractCardRequest(object):
    """The base class for xxxCardRequest classes.

    A CardRequest is used for waitForCard() invocations and specifies what
    kind of smart card an application is waited for.

    Known subclasses: smartcard.pcsc.PCSCCardRequest"""

    def __init__(self, newcardonly=False, readers=None,
                 cardType=None, cardServiceClass=None, timeout=1):
        """Construct new CardRequest.

        newcardonly:        if True, request a new card; default is
                            False, i.e. accepts cards already inserted

        readers:            the list of readers to consider for
                            requesting a card; default is to consider
                            all readers

        cardType:           the smartcard.CardType.CardType to wait for;
                            default is smartcard.CardType.AnyCardType,
                            i.e. the request will succeed with any card

        cardServiceClass:   the specific card service class to create
                            and bind to the card;default is to create
                            and bind a smartcard.PassThruCardService

        timeout:            the time in seconds we are ready to wait for
                            connecting to the requested card.  default
                            is to wait one second; to wait forever, set
                            timeout to None
        """
        self.newcardonly = newcardonly
        self.readersAsked = readers
        self.cardType = cardType
        self.cardServiceClass = cardServiceClass
        self.timeout = timeout

        # if no CardType requeted, use AnyCardType
        if None == self.cardType:
            self.cardType = AnyCardType()

        # if no card service requested, use pass-thru card service
        if None == self.cardServiceClass:
            self.cardServiceClass = PassThruCardService

    def getReaders(self):
        """Returns the list or readers on which to wait for cards."""
        # if readers not given, use all readers
        if None == self.readersAsked:
            return smartcard.System.readers()
        else:
            return self.readersAsked

    def waitforcard(self):
        """Wait for card insertion and returns a card service."""
        pass

    def waitforcardevent(self):
        """Wait for card insertion or removal."""
        pass
