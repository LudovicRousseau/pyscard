"""ReaderFactory: creates smartcard readers.

__author__ = "gemalto http://www.gemalto.com"

Factory pattern implementation borrowed from
Thinking in Python, Bruce Eckel,
http://mindview.net/Books/TIPython

The code to instanciate the reader Factory() has
been updated to dynamically load the module with
Robert Brewer ClassLoader.py.

Copyright 2001-2010 gemalto
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

from smartcard.ClassLoader import get_class


class ReaderFactory:
    """Class to create readers from reader type id."""

    factories = {}

    def addFactory(id, ReaderFactory):
        """Static method to add a ReaderFactory associated to a reader id."""
        ReaderFactory.factories.put[id] = ReaderFactory
    addFactory = staticmethod(addFactory)

    # A Template Method:
    def createReader(clazz, readername):
        """Static method to create a reader from a reader clazz.

        module:     the python module that contains the reader class
        clazz:      the reader class name
        readername: the reader name
        """
        if not ReaderFactory.factories.has_key(clazz):
            ReaderFactory.factories[clazz] = get_class(clazz).Factory()
        return ReaderFactory.factories[clazz].create(readername)
    createReader = staticmethod(createReader)
