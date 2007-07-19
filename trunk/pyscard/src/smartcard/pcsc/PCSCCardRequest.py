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

import threading, time

from smartcard.AbstractCardRequest import AbstractCardRequest
from smartcard.Exceptions import CardRequestTimeoutException, CardRequestException
from smartcard.pcsc.PCSCReader import PCSCReader
from smartcard import Card

from smartcard.scard import *

def signalEvent( evt ):
    evt.set()

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

        # if timeout is None, translate to scard.INFINITE
        if None==self.timeout:
            self.timeout=INFINITE
        # otherwise, from seconds to milliseconds
        else:
            self.timeout=int( self.timeout )

    def getReaderNames( self ):
        """Returns the list of PCSC reader names as strings."""
        # PCSC GetStatusChange is expecting a list of strings
        readernames=[]
        for reader in self.getReaders():
            readernames.append( str(reader) )
        return readernames

    def waitforcard( self ):
        """Wait for card insertion and returns a card service."""
        AbstractCardRequest.waitforcard( self )
        hresult, hcontext = SCardEstablishContext( SCARD_SCOPE_USER )
        if hresult!=0:
            raise CardRequestException( 'Failed to establish context: ' + SCardGetErrorMessage(hresult) )

        cardfound=False
        readerstates = {}

        evt = threading.Event()
        # for non infinite timeout, a timer will signal the end of the time-out
        if self.timeout!=INFINITE:
            timer = threading.Timer( self.timeout, signalEvent, [evt] )


        # initialize reader states and locate current cards in readers
        readernames = self.getReaderNames()
        for i in xrange( len(readernames) ):
            # create a dictionary entry for new readers
            if not readerstates.has_key( str(readernames[i] ) ):
                readerstates[ str(readernames[i]) ] = ( str(readernames[i]), SCARD_STATE_UNAWARE )
        # remove dictionary entry for readers that disappeared
        for oldreader in readerstates.keys():
            if oldreader not in readernames:
                del readerstates[oldreader]
        if {}!=readerstates:
            hresult, newstates = SCardGetStatusChange( hcontext, 0, readerstates.values() )
        else:
            hresult=0
            newstates=[]
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
                            timer.cancel()
                            return self.cardServiceClass( reader.createConnection() )


        # initialize state dictionary
        newstatedict={}

        # start timer
        timer.start()
        while not evt.isSet() and not cardfound:

            # update state dictionary
            for state in newstates:
                readername, eventstate, atr = state
                newstatedict[readername] = state

            # update list of current readers
            readernames = self.getReaderNames()
            for i in xrange( len(readernames) ):
                # create a dictionary entry for new readers
                if not newstatedict.has_key( str(readernames[i] ) ):
                    newstatedict[ str(readernames[i]) ] = ( str(readernames[i]), SCARD_STATE_UNAWARE )
            # remove dictionary entry for readers that disappeared
            for oldreader in newstatedict.keys():
                if oldreader not in readernames:
                    del newstatedict[oldreader]

            # if a new card insertion is requested, wait for card insertion
            if {}!=newstatedict:
                hresult, newstates = SCardGetStatusChange( hcontext, 100, newstatedict.values() )
            else:
                hresult = SCARD_E_TIMEOUT
                newstates=[]
                time.sleep(0.1)

            # real time-out, e.g. the timer has been set
            if SCARD_E_TIMEOUT==hresult and evt.isSet():
                timedout=True
                raise CardRequestTimeoutException()

            # this is a polling time-out of 100ms, make a new iteration
            elif SCARD_E_TIMEOUT==hresult:
                timedout=True

            # some error happened
            elif 0!=hresult:
                timer.cancel()
                raise CardRequestException( 'Failed to get status change ' + SCardGetErrorMessage(hresult) )

            # something changed!
            else:
                for state in newstates:
                    readername, eventstate, atr = state
                    if eventstate & SCARD_STATE_PRESENT and eventstate & SCARD_STATE_CHANGED:
                        reader=PCSCReader(readername)
                        if self.cardType.matches( atr, reader ):
                            if self.cardServiceClass.supports( 'dummy' ):
                                cardfound=True
                                timer.cancel()
                                return self.cardServiceClass( reader.createConnection() )

        try:
            pass
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

            evt = threading.Event()
            # for non infinite timeout, a timer will signal the end of the time-out
            if self.timeout!=INFINITE:
                timer = threading.Timer( self.timeout, signalEvent, [evt] )

            # get status change until time-out, e.g. evt is set
            readerstates = {}
            while not evt.isSet():

                timer.start()

                # reinitialize at each iteration just in case a new reader appeared
                readernames = self.getReaderNames()
                for i in xrange( len(readernames) ):
                    # create a dictionary entry for new readers
                    if not readerstates.has_key( str(readernames[i] ) ):
                        readerstates[ str(readernames[i]) ] = ( str(readernames[i]), SCARD_STATE_UNAWARE )
                # remove dictionary entry for readers that disappeared
                for oldreader in readerstates.keys():
                    if oldreader not in readernames:
                        del readerstates[oldreader]

                # get status change every 100ms
                hresult, newstates = SCardGetStatusChange( hcontext, 100, readerstates.values() )

                # this is a real time-out, e.g. the event has been set
                if SCARD_E_TIMEOUT==hresult and evt.isSet():
                    raise CardRequestTimeoutException()

                # this is a polling time-out of 100ms, make a new iteration
                elif SCARD_E_TIMEOUT==hresult:
                    pass

                # some real error happened
                elif 0!=hresult:
                    timer.cancel()
                    raise CardRequestException( 'Failed to get status change ' + SCardGetErrorMessage(hresult) )

                # something changed!
                else:
                    for state in newstates:
                        readername, eventstate, atr = state
                        if eventstate & SCARD_STATE_PRESENT and eventstate & SCARD_STATE_CHANGED:
                            presentcards.append( Card.Card( readername, atr ) )
                    timer.cancel()

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








