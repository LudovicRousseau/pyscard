"""Smartcard system utility functions and classes.

Manages smartcard readers and reader groups.

__author__ = "gemalto http://www.gemalto.com"

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
import smartcard.reader.ReaderFactory
import smartcard.pcsc.PCSCReaderGroups


def readers(groups=[]):
    """Returns the list of smartcard readers in groups.

    If group is not specified, returns the list of all smartcard readers.

    import smartcard
    r=smartcard.readers()
    r=smartcard.readers(['SCard$DefaultReaders', 'MyReaderGroup'])
    """

    return smartcard.reader.ReaderFactory.ReaderFactory.readers(groups)


def readergroups():
    """Returns the list of reader groups."""

    return smartcard.pcsc.PCSCReaderGroups.PCSCReaderGroups().instance


# for legacy only
def listReaders():
    """Returns the list of smartcard readers.

    Deprecated - Use smartcard.System.readers() instead.
    """
    zreaders = []
    for reader in readers():
        zreaders.append(str(reader))
    return zreaders


if __name__ == '__main__':
    print(readers())
    print(readers(['SCard$DefaultReaders']))
    print(readergroups())
