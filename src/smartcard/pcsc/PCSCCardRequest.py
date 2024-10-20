"""PCSC Smartcard request.

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

import threading
from datetime import datetime

from smartcard import Card
from smartcard.AbstractCardRequest import AbstractCardRequest
from smartcard.Exceptions import (
    CardRequestException,
    CardRequestTimeoutException,
    ListReadersException,
)
from smartcard.pcsc.PCSCExceptions import (
    EstablishContextException,
    ReleaseContextException,
)
from smartcard.pcsc.PCSCReader import PCSCReader
from smartcard.scard import *


class PCSCCardRequest(AbstractCardRequest):
    """PCSC CardRequest class."""

    def __init__(
        self,
        newcardonly=False,
        readers=None,
        cardType=None,
        cardServiceClass=None,
        timeout=1,
    ):
        """Construct new PCSCCardRequest.

        @param newcardonly: if C{True}, request a new card. default is
        C{False}, i.e. accepts cards already inserted

        @param readers: the list of readers to consider for requesting a
        card default is to consider all readers

        @param cardType: the L{CardType} class to wait for; default is
        L{AnyCardType}, i.e.  the request will returns with new or already
        inserted cards

        @param cardServiceClass: the specific card service class to
        create and bind to the card default is to create and bind a
        L{PassThruCardService}

        @param timeout: the time in seconds we are ready to wait for
        connecting to the requested card.  default is to wait one second
        to wait forever, set timeout to C{None}
        """
        AbstractCardRequest.__init__(
            self, newcardonly, readers, cardType, cardServiceClass, timeout
        )

        # if timeout is None, translate to scard.INFINITE
        if self.timeout is None:
            self.timeout = INFINITE
        # otherwise, from seconds to milliseconds
        else:
            self.timeout = int(self.timeout * 1000)

        hresult, self.hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        if hresult != SCARD_S_SUCCESS:
            raise EstablishContextException(hresult)
        self.evt = threading.Event()
        self.hresult = SCARD_S_SUCCESS
        self.readerstates = {}
        self.newstates = []
        self.timeout_init = self.timeout

    def __del__(self):
        hresult = SCardReleaseContext(self.hcontext)
        if hresult != SCARD_S_SUCCESS:
            raise ReleaseContextException(hresult)
        self.hcontext = -1

    def getReaderNames(self):
        """Returns the list of PCSC readers on which to wait for cards."""

        # get inserted readers
        hresult, pcscreaders = SCardListReaders(self.hcontext, [])

        # renew the context in case PC/SC was stopped
        # this happens on Windows when the last reader is disconnected
        if hresult in (SCARD_E_SERVICE_STOPPED, SCARD_E_NO_SERVICE):
            hresult = SCardReleaseContext(self.hcontext)
            if hresult != SCARD_S_SUCCESS:
                raise ReleaseContextException(hresult)
            hresult, self.hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
            if hresult != SCARD_S_SUCCESS:
                raise EstablishContextException(hresult)
            hresult, pcscreaders = SCardListReaders(self.hcontext, [])
        if SCARD_E_NO_READERS_AVAILABLE == hresult:
            return []
        if SCARD_S_SUCCESS != hresult:
            raise ListReadersException(hresult)

        readers = []

        # if no readers asked, use all inserted readers
        if self.readersAsked is None:
            readers = pcscreaders

        # otherwise use only the asked readers that are inserted
        else:
            for reader in self.readersAsked:
                if not isinstance(reader, str):
                    reader = str(reader)
                if reader in pcscreaders:
                    readers = readers + [reader]

        return readers

    # thread waiting for a change
    # the main thread will handle a possible KeyboardInterrupt
    def getStatusChange(self):
        self.hresult, self.newstates = SCardGetStatusChange(
            self.hcontext, self.timeout, list(self.readerstates.values())
        )
        self.evt.set()

    def waitforcard(self):
        """Wait for card insertion and returns a card service."""
        AbstractCardRequest.waitforcard(self)
        cardfound = False

        # create a dictionary entry for new readers
        readerstates = {}
        readernames = self.getReaderNames()
        # add PnP special reader
        readernames.append("\\\\?PnP?\\Notification")

        for reader in readernames:
            if reader not in readerstates:
                readerstates[reader] = (reader, SCARD_STATE_UNAWARE)

        # call SCardGetStatusChange only if we have some readers
        if {} != readerstates:
            hresult, newstates = SCardGetStatusChange(
                self.hcontext, 0, list(readerstates.values())
            )
        else:
            hresult = SCARD_S_SUCCESS
            newstates = []

        # we can expect normally time-outs or reader
        # disappearing just before the call
        # otherwise, raise exception on error
        if (
            SCARD_S_SUCCESS != hresult
            and SCARD_E_TIMEOUT != hresult
            and SCARD_E_UNKNOWN_READER != hresult
        ):
            raise CardRequestException(
                "Failed to SCardGetStatusChange " + SCardGetErrorMessage(hresult),
                hresult=hresult,
            )

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
                        if self.cardServiceClass.supports("dummy"):
                            cardfound = True
                            return self.cardServiceClass(reader.createConnection())

        startDate = datetime.now()
        self.timeout = self.timeout_init
        while not cardfound:

            # create a dictionary entry for new readers
            readernames = self.getReaderNames()

            if self.readersAsked is None:
                # add PnP special reader
                readernames.append("\\\\?PnP?\\Notification")

            for reader in readernames:
                if reader not in readerstates:
                    readerstates[reader] = (reader, SCARD_STATE_UNAWARE)

            # remove dictionary entry for readers that disappeared
            for oldreader in list(readerstates.keys()):
                if oldreader not in readernames:
                    del readerstates[oldreader]

            # wait for card insertion
            self.readerstates = readerstates
            waitThread = threading.Thread(target=self.getStatusChange)
            waitThread.start()

            # the main thread handles a possible KeyboardInterrupt
            try:
                waitThread.join()
            except KeyboardInterrupt:
                hresult = SCardCancel(self.hcontext)
                if hresult != SCARD_S_SUCCESS:
                    raise CardRequestException(
                        "Failed to SCardCancel " + SCardGetErrorMessage(hresult),
                        hresult=hresult,
                    )

            # wait for the thread to finish in case of KeyboardInterrupt
            self.evt.wait(timeout=None)

            # get values set in the getStatusChange thread
            hresult = self.hresult
            newstates = self.newstates

            # compute remaining timeout
            if self.timeout != INFINITE:
                delta = datetime.now() - startDate
                self.timeout -= int(delta.total_seconds() * 1000)
                if self.timeout < 0:
                    self.timeout = 0

            # time-out
            if hresult in (SCARD_E_TIMEOUT, SCARD_E_CANCELLED):
                raise CardRequestTimeoutException(hresult=hresult)

            # reader vanished before or during the call
            elif SCARD_E_UNKNOWN_READER == hresult:
                pass

            # this happens on Windows when the last reader is disconnected
            elif hresult in (SCARD_E_SYSTEM_CANCELLED, SCARD_E_NO_SERVICE):
                pass

            # some error happened
            elif SCARD_S_SUCCESS != hresult:
                raise CardRequestException(
                    "Failed to get status change " + SCardGetErrorMessage(hresult),
                    hresult=hresult,
                )

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
                        if oldstate & SCARD_STATE_PRESENT and eventstate & (
                            SCARD_STATE_CHANGED | SCARD_STATE_PRESENT
                        ):
                            eventstate = eventstate & (0xFFFFFFFF ^ SCARD_STATE_CHANGED)

                    if (
                        self.newcardonly
                        and eventstate & SCARD_STATE_PRESENT
                        and eventstate & SCARD_STATE_CHANGED
                    ) or (not self.newcardonly and eventstate & SCARD_STATE_PRESENT):
                        reader = PCSCReader(readername)
                        if self.cardType.matches(atr, reader):
                            if self.cardServiceClass.supports("dummy"):
                                cardfound = True
                                return self.cardServiceClass(reader.createConnection())

                    # update state dictionary
                    readerstates[readername] = (readername, eventstate)

    def waitforcardevent(self):
        """Wait for card insertion or removal."""
        AbstractCardRequest.waitforcardevent(self)
        presentcards = []
        readerstates = {}

        startDate = datetime.now()
        eventfound = False
        self.timeout = self.timeout_init
        previous_readernames = self.getReaderNames()
        while not eventfound:

            # reinitialize at each iteration just in case a new reader appeared
            _readernames = self.getReaderNames()
            readernames = _readernames

            if self.readersAsked is None:
                # add PnP special reader
                readernames.append("\\\\?PnP?\\Notification")

            readerstates = {}
            for reader in readernames:
                # create a dictionary entry for new readers
                readerstates[reader] = (reader, SCARD_STATE_UNAWARE)

            hresult, newstates = SCardGetStatusChange(
                self.hcontext, 0, list(readerstates.values())
            )

            # check if a new reader with a card has just been connected
            for state in newstates:
                readername, eventstate, _ = state

                # the reader is a new one
                if readername not in previous_readernames:
                    if eventstate & SCARD_STATE_PRESENT:
                        eventfound = True

            if eventfound:
                break

            # update previous readers list
            previous_readernames = _readernames

            # update readerstate
            for state in newstates:
                readername, eventstate, atr = state
                readerstates[readername] = (readername, eventstate)

            # wait for card insertion
            self.readerstates = readerstates
            waitThread = threading.Thread(target=self.getStatusChange)
            waitThread.start()

            # the main thread handles a possible KeyboardInterrupt
            try:
                waitThread.join()
            except KeyboardInterrupt:
                hresult = SCardCancel(self.hcontext)
                if hresult != SCARD_S_SUCCESS:
                    raise CardRequestException(
                        "Failed to SCardCancel " + SCardGetErrorMessage(hresult),
                        hresult=hresult,
                    )

            # wait for the thread to finish in case of KeyboardInterrupt
            self.evt.wait(timeout=None)

            # get values set in the getStatusChange thread
            hresult = self.hresult
            newstates = self.newstates

            # compute remaining timeout
            if self.timeout != INFINITE:
                delta = datetime.now() - startDate
                self.timeout -= int(delta.total_seconds() * 1000)
                if self.timeout < 0:
                    self.timeout = 0

            # time-out
            if hresult in (SCARD_E_TIMEOUT, SCARD_E_CANCELLED):
                raise CardRequestTimeoutException(hresult=hresult)

            # the reader was unplugged during the loop
            elif SCARD_E_UNKNOWN_READER == hresult:
                pass

            # this happens on Windows when the last reader is disconnected
            elif hresult in (SCARD_E_SYSTEM_CANCELLED, SCARD_E_NO_SERVICE):
                pass

            # some error happened
            elif SCARD_S_SUCCESS != hresult:
                raise CardRequestException(
                    "Failed to get status change " + SCardGetErrorMessage(hresult),
                    hresult=hresult,
                )

            # something changed!
            else:
                for state in newstates:
                    readername, eventstate, atr = state

                    # ignore Pnp reader
                    if readername == "\\\\?PnP?\\Notification":
                        continue

                    _, oldstate = readerstates[readername]

                    # the status can change on a card already inserted, e.g.
                    # unpowered, in use, ... Clear the state changed bit if
                    # the card was already inserted and is still inserted
                    if (
                        oldstate & SCARD_STATE_PRESENT
                        and eventstate & (SCARD_STATE_CHANGED | SCARD_STATE_PRESENT)
                        == SCARD_STATE_CHANGED | SCARD_STATE_PRESENT
                    ):
                        eventstate = eventstate & (0xFFFFFFFF ^ SCARD_STATE_CHANGED)

                    if eventstate & SCARD_STATE_CHANGED:
                        if (
                            # a reader or a card has been removed
                            oldstate & SCARD_STATE_PRESENT
                            or
                            # a card has been inserted
                            eventstate & SCARD_STATE_PRESENT
                        ):
                            eventfound = True

        # return all the cards present
        for state in newstates:
            readername, eventstate, atr = state
            if readername == "\\\\?PnP?\\Notification":
                continue
            if eventstate & SCARD_STATE_PRESENT:
                presentcards.append(Card.Card(readername, atr))

        return presentcards


if __name__ == "__main__":
    """Small sample illustrating the use of PCSCCardRequest.py."""

    from smartcard.util import toHexString

    print("Insert a new card within 10 seconds")
    cr = PCSCCardRequest(timeout=10, newcardonly=True)
    cs = cr.waitforcard()
    cs.connection.connect()
    print(cs.connection.getReader() + " " + toHexString(cs.connection.getATR()))
    cs.connection.disconnect()
