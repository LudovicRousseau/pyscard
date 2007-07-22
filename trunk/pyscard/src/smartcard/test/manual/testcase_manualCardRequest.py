#! /usr/bin/env python
"""Manual unit tests for smartcard.CardRequest

__author__ = "http://www.gemalto.com"

Copyright 2001-2007 gemalto
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


import string
import time
import unittest

from smartcard.CardConnection import CardConnection
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.CardRequest import CardRequest
from smartcard.CardType import AnyCardType
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.util import toHexString


class testcase_manualCardRequest( unittest.TestCase, CardObserver ):
    """Test case for CardRequest."""


    def setUp( self ):
        self.cardmonitor = CardMonitor()
        self.cardmonitor.addObserver( self )
        self.updated=False

    def tearDown( self ):
        self.cardmonitor.deleteObserver( self )

    def update( self, observable, (addedcards, removedcards) ):
        if not hasattr( self, 'presentcards'):
            self.presentcards={}
        for card in addedcards:
            self.presentcards[`card`]=True
        for card in removedcards:
            del self.presentcards[`card`]
        self.updated=True

    def testcase_CardRequestNewCardAnyCardTypeInfiniteTimeOut( self ):
        """Test smartcard.CardRequest for new card."""

        cardtype = AnyCardType()
        cardrequest = CardRequest( timeout=None, cardType=cardtype, newcardonly=True )

        while not self.updated:
            time.sleep(1)
        print 'please remove all inserted smart cards'
        while {}!=self.presentcards:
            time.sleep(.3)
        print 're-insert any combination of cards six time'
        for i in range( 0, 6 ):
            cardservice = cardrequest.waitforcard()
            cardservice.connection.connect( CardConnection.T0_protocol )
            print cardservice.connection.getReader() + ': ' + toHexString(cardservice.connection.getATR())
            cardservice.connection.disconnect()

    def testcase_CardRequestNewCardAnyCardTypeFiniteTimeOut( self ):
        """Test smartcard.CardRequest for new card."""

        cardtype = AnyCardType()
        cardrequest = CardRequest( timeout=1, cardType=cardtype, newcardonly=True )

        while not self.updated:
            time.sleep(1)
        print 'please remove all inserted smart cards'
        while {}!=self.presentcards:
            time.sleep(.3)
        count=0
        for i in range( 0, 6 ):
            try:
                cardservice = cardrequest.waitforcard()
            except CardRequestTimeoutException,e:
                count=count+1
                print '.',
            print  ''
        self.assertEquals( 6, count )


def suite():
    suite1 = unittest.makeSuite( testcase_manualCardRequest )
    return unittest.TestSuite((suite1))


if __name__ == '__main__':
    unittest.main()

