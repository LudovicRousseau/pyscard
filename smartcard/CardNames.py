"""Card Names class

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
from _bsddb import DBNotFoundError
from bsddb import hashopen
from os import environ
from os.path import join
from pickle import dumps, loads, HIGHEST_PROTOCOL


from smartcard.Synchronization import Synchronization, synchronize
from smartcard.util import toBytes


class __CardNames__(Synchronization):
    """__CardNames__ inner class.

    Stores card names and card types into a bsddb hash database.

    The smartcard.CardNames.CardNames singleton manages the creation
    of the unique instance of this class.
    """

    def __init__(self):
        Synchronization.__init__(self)
        carddb_dir = environ['ALLUSERSPROFILE']
        carddb_file = 'cardnames.bdb'
        carddb_file = join(carddb_dir, carddb_file)
        self.db = hashopen(carddb_file, 'w')

    def __del__(self):
        self.db.sync()
        self.db.close()

    def add(self, cardname, cardtype):
        self.db[cardname] = dumps(cardtype, HIGHEST_PROTOCOL)
        self.db.sync()

    def delete(self, cardname):
        try:
            del self.db[cardname]
        except DBNotFoundError:
            pass

    def dump(self):
        for k, v in list(self.db.items()):
            print(k, repr(loads(v)))

    def find(self, atr, reader=None):
        for k, v in list(self.db.items()):
            if loads(v).matches(atr, reader):
                return k

synchronize(__CardNames__, "add delete dump find")


class CardNames(object):
    """The CardNames organizes cards by a unique name and an associated
    smartcard.CardType.CardType."""

    """The single instance of __CardNames__"""
    instance = None

    def __init__(self):
        """Constructor: create a single instance of __readergroups on
        first call"""
        if CardNames.instance is None:
            CardNames.instance = __CardNames__()

    def __getattr__(self, name):
        """All operators redirected to inner class."""
        return getattr(self.instance, name)


if __name__ == '__main__':
    from smartcard.CardType import ATRCardType

    # define a card by its ATR
    ct = ATRCardType([0x3B, 0x16, 0x94, 0x20, 0x02, 0x01, 0x00, 0x00, 0x0D])

    # create CardName
    cn = CardNames()
    cn.add("Palmera Protect V2", ct)
    cn.dump()
    print(cn.find([0x3B, 0x16, 0x94, 0x20, 0x02, 0x01, 0x00, 0x00, 0x0D]))
    print(cn.find([0x3B, 0x16, 0x94, 0x20, 0x02, 0x01, 0x00, 0x00]))
    cn.delete("Palmera Protect V2")
    print('---------')
    cn.dump()
