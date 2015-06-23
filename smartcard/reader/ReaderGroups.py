"""ReaderGroups manages smart card reader in groups.

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
from smartcard.Exceptions import SmartcardException
from smartcard.ulist import ulist


class BadReaderGroupException(SmartcardException):
    """Raised when trying to add an invalid reader group."""

    def __init__(self):
        SmartcardException.__init__(self, 'Invalid reader group')


class DeleteSCardDefaultReaderGroupException(SmartcardException):
    """Raised when trying to delete SCard$DefaultReaders reader group."""

    def __init__(self):
        SmartcardException.__init__(
            self, 'SCard$DefaultReaders cannot be deleted')


class innerreadergroups(ulist):
    """Smartcard readers groups private class.

    The readergroups singleton manages the creation of the unique
    instance of this class.
    """

    def __init__(self, initlist=None):
        """Retrieve and store list of reader groups"""
        if None == initlist:
            initlist = self.getreadergroups()
        if None != initlist:
            ulist.__init__(self, initlist)
        self.unremovablegroups = []

    def __onadditem__(self, item):
        """Called when a reader group is added."""
        self.addreadergroup(item)

    def __onremoveitem__(self, item):
        """Called when a reader group is added."""
        self.removereadergroup(item)

    def __iter__(self):
        return ulist.__iter__(self)

    def next(self):
        return ulist.__next__(self)

    #
    # abstract methods implemented in subclasses
    #

    def getreadergroups(self):
        """Returns the list of smartcard reader groups."""
        return []

    def addreadergroup(self, newgroup):
        """Add a reader group"""
        if not isinstance(newgroup, type("")):
            raise BadReaderGroupException
        self += newgroup

    def removereadergroup(self, group):
        """Remove a reader group"""
        if not isinstance(group, type("")):
            raise BadReaderGroupException
        self.remove(group)

    def addreadertogroup(self, readername, groupname):
        """Add a reader to a reader group"""
        pass

    def removereaderfromgroup(self, readername, groupname):
        """Remove a reader from a reader group"""
        pass


class readergroups(object):
    """ReadersGroups organizes smart card reader as groups."""

    """The single instance of __readergroups"""
    instance = None
    innerclazz = innerreadergroups

    def __init__(self, initlist=None):
        """Create a single instance of innerreadergroups on first call"""
        if None == readergroups.instance:
            readergroups.instance = self.innerclazz(initlist)

    """All operators redirected to inner class."""

    def __getattr__(self, name):
        return getattr(self.instance, name)


if __name__ == '__main__':
    print(readergroups())

