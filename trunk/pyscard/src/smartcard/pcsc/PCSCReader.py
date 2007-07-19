"""PCSCReader: concrete reader class for PCSC Readers

__author__ = "gemalto http://www.gemalto.com"

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

from smartcard.CardConnectionDecorator import CardConnectionDecorator
from smartcard.reader.ReaderFactory import ReaderFactory
from smartcard.reader.Reader import Reader
from smartcard.pcsc.PCSCCardConnection import PCSCCardConnection
from smartcard.Exceptions import *
from smartcard.pcsc.PCSCExceptions import *
from smartcard.scard import *

def __PCSCreaders__( groups=[] ):
    """Returns the list of PCSC smartcard readers in PCSC group.

    If group is not specified, returns the list of all PCSC smartcard readers.
    """

    # in case we have a string instead of a list
    if isinstance( groups, type("")): groups=[groups]
    try:
        hresult, hcontext=SCardEstablishContext( SCARD_SCOPE_USER )
        if hresult!=0:
            raise EstablishContextException( hresult )
        hresult, readers = SCardListReaders( hcontext, groups )
        if hresult!=0:
            if hresult==SCARD_E_NO_READERS_AVAILABLE:
                readers=[]
            else:
                raise ListReadersException( hresult )
    finally:
        if 0!=hcontext:
            hresult = SCardReleaseContext( hcontext )
            if hresult!=0:
                raise ReleaseContextException( hresult )

    return readers


class PCSCReader( Reader ):
    """PCSC reader class."""
    def __init__( self, readername ):
        """Constructs a new PCSC reader."""
        Reader.__init__( self, readername )

    def addtoreadergroup( self, groupname ):
        """Add reader to a reader group."""

        hresult, hcontext = SCardEstablishContext( SCARD_SCOPE_USER )
        if 0!=hresult:
            raise error, 'Failed to establish context: ' + SCardGetErrorMessage(hresult)
        try:
            hresult = SCardIntroduceReader( hcontext, self.name, self.name )
            if 0!=hresult and SCARD_E_DUPLICATE_READER!=hresult:
                raise error, 'Unable to introduce reader: ' + self.name + ' : ' + SCardGetErrorMessage(hresult)
            hresult = SCardAddReaderToGroup( hcontext, self.name, groupname )
            if hresult!=0:
                raise error, 'Unable to add reader to group: ' + SCardGetErrorMessage(hresult)
        finally:
            hresult = SCardReleaseContext( hcontext )
            if 0!=hresult:
                raise error, 'Failed to release context: ' + SCardGetErrorMessage(hresult)


    def removefromreadergroup( self, groupname ):
        """Remove a reader from a reader group"""

        hresult, hcontext = SCardEstablishContext( SCARD_SCOPE_USER )
        if 0!=hresult:
            raise error, 'Failed to establish context: ' + SCardGetErrorMessage(hresult)
        try:
            hresult = SCardRemoveReaderFromGroup( hcontext, self.name, groupname )
            if hresult!=0:
                raise error, 'Unable to add reader to group: ' + SCardGetErrorMessage(hresult)
        finally:
            hresult = SCardReleaseContext( hcontext )
            if 0!=hresult:
                raise error, 'Failed to release context: ' + SCardGetErrorMessage(hresult)


    def createConnection( self ):
        """Return a card connection thru PCSC reader."""
        return CardConnectionDecorator( PCSCCardConnection( self.name ) )

    class Factory:
        def create(self, readername ):
            return PCSCReader( readername )

def readers( groups=[] ):
    creaders=[]
    for reader in __PCSCreaders__( groups ):
        creaders.append( ReaderFactory.createReader( 'smartcard.pcsc.PCSCReader.PCSCReader', reader ) )
    return creaders

if __name__ == '__main__':
    SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    DF_TELECOM = [0x7F, 0x10]

    creaders=readers()
    cc = creaders[1].createConnection()
    cc.connect()
    data, sw1, sw2 = cc.transmit( SELECT + DF_TELECOM )
    print "%X %X" % (sw1, sw2)


