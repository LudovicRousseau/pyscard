"""PCSC Smartcard request.

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

from smartcard.AbstractCardRequest import AbstractCardRequest
from smartcard.Exceptions import CardRequestTimeoutException, CardRequestException
from smartcard.pcsc.PCSCReader import PCSCReader
from smartcard import Card

from smartcard.scard import *

class PCSCCardRequest(AbstractCardRequest):
    """PCSC CardRequest class."""

    def __init__( self, newcardonly=False, readers=None, cardType=None, cardServiceClass=None, timeout=1 ):
        """Construct new PCSCCardRequest.

        newcardonly:        if True, request a new card
                            default is False, i.e. accepts cards already inserted

        readers:            the list of readers to consider for requesting a card
                            default is to consider all readers

        cardTypeClass:      the CardType class to wait for; default is AnyCardType, i.e.
                            the request will returns with new or already inserted cards

        cardServiceClass:   the specific card service class to create and bind to the card
                            default is to create and bind a PassThruCardService

        timeout:            the time in seconds we are ready to wait for connecting to the
                            requested card.
                            default is to wait one second
                            to wait forever, set timeout to None
        """
        AbstractCardRequest.__init__( self, newcardonly, readers, cardType, cardServiceClass, timeout )

        # PCSC is expecting a list of strings
        self.readernames=[]
        for reader in self.readers:
            self.readernames.append( str(reader) )

        # if timeout is None, translate to scard.INFINITE
        if None==self.timeout:
            self.timeout=INFINITE
        # otherwise, from seconds to milliseconds
        else:
            self.timeout=int(1000*self.timeout)



    def waitforcard( self ):
        """Wait for card insertion and returns a card service."""
        AbstractCardRequest.waitforcard( self )
        hresult, hcontext = SCardEstablishContext( SCARD_SCOPE_USER )
        if hresult!=0:
            raise CardRequestException( 'Failed to establish context: ' + SCardGetErrorMessage(hresult) )

        try:
            timedout=cardfound=False

            # initialize reader states and locate current cards in readers
            readerstates = []
            for i in xrange(len(self.readers)):
                readerstates += [ (str(self.readernames[i]), SCARD_STATE_UNAWARE ) ]
            hresult, newstates = SCardGetStatusChange( hcontext, 0, readerstates )
            if hresult!=0:
                raise CardRequestException( 'Failed to SCardGetStatusChange ' + SCardGetErrorMessage(hresult) )


            # if a new card is not requested, just return the first available
            if not self.newcardonly:
                for state in newstates:
                    readername, eventstate, atr = state
                    if eventstate & SCARD_STATE_PRESENT:
                        reader=PCSCReader(readername)
                        if self.cardType.matches( atr, reader ):
                            if self.cardServiceClass.supports( 'dummy' ):
                                cardfound=True
                                return self.cardServiceClass( reader.createConnection() )

            while not timedout and not cardfound:

                # if a new card insertion is requested, wait for card insertion
                hresult, newstates = SCardGetStatusChange( hcontext, self.timeout, newstates )
                if SCARD_E_TIMEOUT==hresult:
                    timedout=True
                    raise CardRequestTimeoutException()
                elif 0!=hresult:
                    raise CardRequestException( 'Failed to get status change ' + SCardGetErrorMessage(hresult) )
                else:
                    for state in newstates:
                        readername, eventstate, atr = state
                        if eventstate & SCARD_STATE_PRESENT and eventstate & SCARD_STATE_CHANGED:
                            reader=PCSCReader(readername)
                            if self.cardType.matches( atr, reader ):
                                if self.cardServiceClass.supports( 'dummy' ):
                                    cardfound=True
                                    return self.cardServiceClass( reader.createConnection() )

        finally:
            hresult = SCardReleaseContext( hcontext )
            if hresult!=0:
                raise CardRequestException( 'Failed to release context: ' + SCardGetErrorMessage(hresult) )


    def waitforcardevent( self ):
        """Wait for card insertion or removal."""
        AbstractCardRequest.waitforcard( self )
        presentcards = []
        hresult, hcontext = SCardEstablishContext( SCARD_SCOPE_USER )
        if hresult!=0:
            raise CardRequestException( 'Failed to establish context: ' + SCardGetErrorMessage(hresult) )

        try:
            readerstates = []
            for i in xrange(len(self.readers)):
                readerstates += [ (str(self.readernames[i]), SCARD_STATE_UNAWARE ) ]

            hresult, newstates = SCardGetStatusChange( hcontext, self.timeout, readerstates )
            if SCARD_E_TIMEOUT==hresult:
                raise CardRequestTimeoutException()
            elif 0!=hresult:
                raise CardRequestException( 'Failed to get status change ' + SCardGetErrorMessage(hresult) )
            else:
                for state in newstates:
                    readername, eventstate, atr = state
                    if eventstate & SCARD_STATE_PRESENT and eventstate & SCARD_STATE_CHANGED:
                        presentcards.append( Card.Card( readername, atr ) )

        finally:
            hresult = SCardReleaseContext( hcontext )
            if hresult!=0:
                raise CardRequestException( 'Failed to release context: ' + SCardGetErrorMessage(hresult) )
            return presentcards


if __name__ == '__main__':
    """Small sample illustrating the use of PCSCCardRequest.py."""

    from smartcard.util import toHexString
    print 'Insert a new card within 10 seconds'
    cr=PCSCCardRequest( timeout=10, newcardonly=True )
    cs = cr.waitforcard()
    cs.connection.connect()
    print cs.connection.getReader(), toHexString(cs.connection.getATR())
    cs.connection.disconnect()








