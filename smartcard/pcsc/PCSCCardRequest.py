"""PCSC Smartcard request.

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
import threading
import time

from smartcard.AbstractCardRequest import AbstractCardRequest
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.Exceptions import CardRequestException, ListReadersException
from smartcard.pcsc.PCSCReader import PCSCReader
from smartcard.pcsc.PCSCContext import PCSCContext
from smartcard import Card

from smartcard.scard import *


def signalEvent(evt, isInfinite):
    if not isInfinite:
        evt.set()


class PCSCCardRequest(AbstractCardRequest):
    """PCSC CardRequest class."""

    def __init__(self, newcardonly=False, readers=None,
                 cardType=None, cardServiceClass=None, timeout=1):
        """Construct new PCSCCardRequest.

        @param newcardonly: if True, request a new card default is
        False, i.e. accepts cards already inserted

        @param readers: the list of readers to consider for requesting a
        card default is to consider all readers

        @param cardType: the CardType class to wait for; default is
        AnyCardType, i.e.  the request will returns with new or already
        inserted cards

        @param cardServiceClass: the specific card service class to
        create and bind to the card default is to create and bind a
        PassThruCardService

        @param timeout: the time in seconds we are ready to wait for
        connecting to the requested card.  default is to wait one second
        to wait forever, set timeout to None
        """
        AbstractCardRequest.__init__(
            self, newcardonly, readers, cardType, cardServiceClass, timeout)

        # polling interval in s for SCardGetStatusChange
        self.pollinginterval = 0.1

        # if timeout is None, translate to scard.INFINITE
        if None == self.timeout:
            self.timeout = INFINITE
        # otherwise, from seconds to milliseconds
        else:
            self.timeout = int(self.timeout)

        self.hcontext = PCSCContext().getContext()

    def getReaderNames(self):
        """Returns the list or PCSC readers on which to wait for cards."""

        # get inserted readers
        hresult, pcscreaders = SCardListReaders(self.hcontext, [])
        if 0 != hresult and SCARD_E_NO_READERS_AVAILABLE != hresult:
            raise ListReadersException(hresult)

        readers = []

        # if no readers asked, use all inserted readers
        if None == self.readersAsked:
            readers = pcscreaders

        # otherwise use only the asked readers that are inserted
        else:
            for reader in self.readersAsked:
                if not isinstance(reader, type("")):
                    reader = str(reader)
                if reader in pcscreaders:
                    readers = readers + [reader]

        return readers

    def waitforcard(self):
        """Wait for card insertion and returns a card service."""
        AbstractCardRequest.waitforcard(self)
        cardfound = False

        # for non infinite timeout, a timer will signal
        # the end of the time-out by setting the evt event
        evt = threading.Event()
        if INFINITE == self.timeout:
            timertimeout = 1
        else:
            timertimeout = self.timeout
        timer = threading.Timer(
            timertimeout, signalEvent, [evt, INFINITE == self.timeout])

        # create a dictionary entry for new readers
        readerstates = {}
        readernames = self.getReaderNames()
        for reader in readernames:
            if not reader in readerstates:
                readerstates[reader] = (reader, SCARD_STATE_UNAWARE)

        # remove dictionary entry for readers that disappeared
        for oldreader in list(readerstates.keys()):
            if oldreader not in readernames:
                del readerstates[oldreader]

        # call SCardGetStatusChange only if we have some readers
        if {} != readerstates:
            hresult, newstates = SCardGetStatusChange(
                self.hcontext, 0, list(readerstates.values()))
        else:
            hresult = 0
            newstates = []

        # we can expect normally time-outs or reader
        # disappearing just before the call
        # otherwise, raise execption on error
        if 0 != hresult and \
            SCARD_E_TIMEOUT != hresult and \
            SCARD_E_UNKNOWN_READER != hresult:
                raise CardRequestException(
                    'Failed to SCardGetStatusChange ' + \
                    SCardGetErrorMessage(hresult))

        # in case of timeout or reader disappearing,
        # the content of the states is useless
        # in which case we clear the changed bit
        if SCARD_E_TIMEOUT == hresult or SCARD_E_UNKNOWN_READER == hresult:
            for state in newstates:
                state[1] = state[1] & (0xFFFFFFFF ^ SCARD_STATE_CHANGED)

        # update readerstate
        for state in newstates:
            readername, eventstate, atr = state
            readerstates[readername] = (readername, eventstate)

        # if a new card is not requested, just return the first available
        if not self.newcardonly:
            for state in newstates:
                readername, eventstate, atr = state
                if eventstate & SCARD_STATE_PRESENT:
                    reader = PCSCReader(readername)
                    if self.cardType.matches(atr, reader):
                        if self.cardServiceClass.supports('dummy'):
                            cardfound = True
                            return self.cardServiceClass(
                                    reader.createConnection())

        timerstarted = False
        while not evt.isSet() and not cardfound:

            if not timerstarted:
                timerstarted = True
                timer.start()

            time.sleep(self.pollinginterval)

            # create a dictionary entry for new readers
            readernames = self.getReaderNames()
            for reader in readernames:
                if not reader in readerstates:
                    readerstates[reader] = (reader, SCARD_STATE_UNAWARE)

            # remove dictionary entry for readers that disappeared
            for oldreader in list(readerstates.keys()):
                if oldreader not in readernames:
                    del readerstates[oldreader]

            # wait for card insertion
            if {} != readerstates:
                hresult, newstates = SCardGetStatusChange(
                    self.hcontext, 0, list(readerstates.values()))
            else:
                hresult = SCARD_E_TIMEOUT
                newstates = []

            # time-out
            if SCARD_E_TIMEOUT == hresult:
                if evt.isSet():
                    raise CardRequestTimeoutException()

            # reader vanished before or during the call
            elif SCARD_E_UNKNOWN_READER == hresult:
                pass

            # some error happened
            elif 0 != hresult:
                timer.cancel()
                raise CardRequestException(
                    'Failed to get status change ' + \
                    SCardGetErrorMessage(hresult))

            # something changed!
            else:

                # check if we have to return a match, i.e.
                # if no new card in inserted and there is a card found
                # or if a new card is requested, and there is a change+present
                for state in newstates:
                    readername, eventstate, atr = state
                    r, oldstate = readerstates[readername]

                    # the status can change on a card already inserted, e.g.
                    # unpowered, in use, ...
                    # if a new card is requested, clear the state changed bit
                    # if the card was already inserted and is still inserted
                    if self.newcardonly:
                        if oldstate & SCARD_STATE_PRESENT and \
                            eventstate & \
                                (SCARD_STATE_CHANGED | SCARD_STATE_PRESENT):
                            eventstate = eventstate & \
                                (0xFFFFFFFF ^ SCARD_STATE_CHANGED)

                    if (self.newcardonly and \
                            eventstate & SCARD_STATE_PRESENT and \
                            eventstate & SCARD_STATE_CHANGED) or \
                        (not self.newcardonly and \
                         eventstate & SCARD_STATE_PRESENT):
                        reader = PCSCReader(readername)
                        if self.cardType.matches(atr, reader):
                            if self.cardServiceClass.supports('dummy'):
                                cardfound = True
                                timer.cancel()
                                return self.cardServiceClass(
                                        reader.createConnection())

                    # update state dictionary
                    readerstates[readername] = (readername, eventstate)

            if evt.isSet():
                raise CardRequestTimeoutException()

    def waitforcardevent(self):
        """Wait for card insertion or removal."""
        AbstractCardRequest.waitforcardevent(self)
        presentcards = []
        evt = threading.Event()

        # for non infinite timeout, a timer will signal the end of the time-out
        if INFINITE == self.timeout:
            timertimeout = 1
        else:
            timertimeout = self.timeout
        timer = threading.Timer(
            timertimeout, signalEvent, [evt, INFINITE == self.timeout])

        # get status change until time-out, e.g. evt is set
        readerstates = {}
        timerstarted = False

        while not evt.isSet():

            if not timerstarted:
                timerstarted = True
                timer.start()

            time.sleep(self.pollinginterval)

            # reinitialize at each iteration just in case a new reader appeared
            readernames = self.getReaderNames()
            for reader in readernames:
                # create a dictionary entry for new readers
                if not reader in readerstates:
                    readerstates[reader] = (reader, SCARD_STATE_UNAWARE)
            # remove dictionary entry for readers that disappeared
            for oldreader in list(readerstates.keys()):
                if oldreader not in readernames:
                    del readerstates[oldreader]

            # get status change
            if {} != readerstates:
                hresult, newstates = SCardGetStatusChange(
                    self.hcontext, 0, list(readerstates.values()))
            else:
                hresult = 0
                newstates = []

            # time-out
            if SCARD_E_TIMEOUT == hresult:
                if evt.isSet():
                    raise CardRequestTimeoutException()

            # the reader was unplugged during the loop
            elif SCARD_E_UNKNOWN_READER == hresult:
                pass

            # some error happened
            elif 0 != hresult:
                timer.cancel()
                raise CardRequestException(
                    'Failed to get status change ' + \
                    SCardGetErrorMessage(hresult))

            # something changed!
            else:
                timer.cancel()
                for state in newstates:
                    readername, eventstate, atr = state
                    r, oldstate = readerstates[readername]

                    # the status can change on a card already inserted, e.g.
                    # unpowered, in use, ... Clear the state changed bit if
                    # the card was already inserted and is still inserted
                    if oldstate & SCARD_STATE_PRESENT and \
                        eventstate & \
                            (SCARD_STATE_CHANGED | SCARD_STATE_PRESENT):
                        eventstate = eventstate & \
                            (0xFFFFFFFF ^ SCARD_STATE_CHANGED)

                    if eventstate & SCARD_STATE_PRESENT and \
                       eventstate & SCARD_STATE_CHANGED:
                        presentcards.append(Card.Card(readername, atr))
                return presentcards

        if evt.isSet():
            raise CardRequestTimeoutException()

if __name__ == '__main__':
    """Small sample illustrating the use of PCSCCardRequest.py."""

    from smartcard.util import toHexString
    print('Insert a new card within 10 seconds')
    cr = PCSCCardRequest(timeout=10, newcardonly=True)
    cs = cr.waitforcard()
    cs.connection.connect()
    print(cs.connection.getReader() + ' ' + toHexString(cs.connection.getATR()))
    cs.connection.disconnect()

