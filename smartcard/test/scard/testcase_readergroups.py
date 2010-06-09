#! /usr/bin/env python
"""Unit tests for SCardxxx readers and readergroups methods.

This test case can be executed individually, or with all other test cases
thru testsuite_scard.py.

__author__ = "http://www.gemalto.com"

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


import unittest
from smartcard.scard import *

# import local_config for reader/card configuration
# configcheck.py is generating local_config.py in
# the test suite.
import sys
sys.path += ['..']

try:
    from local_config import expectedReaders
except:
    print 'execute test suite first to generate the local_config.py file'
    sys.exit()


expectedGroups = ['SCard$DefaultReaders']


class testcase_readergroups(unittest.TestCase):
    """Test scard reader groups API"""

    def setUp(self):
        hresult, self.hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
        self.assertEquals(hresult, 0)

    def tearDown(self):
        hresult = SCardReleaseContext(self.hcontext)
        self.assertEquals(hresult, 0)

    def test_listReaders(self):

        # list current readers and compare with expected list
        hresult, readers = SCardListReaders(self.hcontext, [])
        self.assertEquals(hresult, 0)
        for i in xrange(len(expectedReaders)):
            self.assertEquals(readers[i], expectedReaders[i])

        # list current reader groups and compare with expected list
        hresult, readerGroups = SCardListReaderGroups(self.hcontext)
        self.assertEquals(hresult, 0)
        for i in xrange(len(expectedGroups)):
            self.assertEquals(readerGroups[i], expectedGroups[i])

        if 'winscard' == resourceManager:
            # add a new group
            newgroup = 'SCard$MyOwnGroup'
            expectedGroups.append(newgroup)

            hresult = SCardIntroduceReaderGroup(self.hcontext, newgroup)
            self.assertEquals(hresult, 0)

            dummyreader = readers[0] + ' alias'
            hresult = SCardIntroduceReader(self.hcontext, dummyreader, readers[0])
            self.assertEquals(hresult, 0)

            hresult = SCardAddReaderToGroup(self.hcontext, dummyreader, newgroup)
            self.assertEquals(hresult, 0)

            hresult, readerGroups = SCardListReaderGroups(self.hcontext)
            self.assertEquals(hresult, 0)
            for i in xrange(len(expectedGroups)):
                self.assertEquals(readerGroups[i], expectedGroups[i])

            # list readers in new group
            hresult, newreaders = SCardListReaders(self.hcontext, [newgroup])
            self.assertEquals(hresult, 0)
            self.assertEquals(newreaders[0], dummyreader)

            # remove reader from new group
            hresult = SCardRemoveReaderFromGroup(self.hcontext, dummyreader, newgroup)
            self.assertEquals(hresult, 0)

            hresult, readerGroups = SCardListReaderGroups(self.hcontext)
            self.assertEquals(hresult, 0)

            expectedGroups.remove(newgroup)
            for i in xrange(len(expectedGroups)):
                self.assertEquals(readerGroups[i], expectedGroups[i])

            hresult = SCardForgetReaderGroup(self.hcontext, newgroup)
            self.assertEquals(hresult, 0)

            hresult, readerGroups = SCardListReaderGroups(self.hcontext)
            self.assertEquals(hresult, 0)
            for i in xrange(len(expectedGroups)):
                self.assertEquals(readerGroups[i], expectedGroups[i])

            hresult = SCardForgetReader(self.hcontext, dummyreader)
            self.assertEquals(hresult, 0)


def suite():
    suite1 = unittest.makeSuite(testcase_readergroups)
    return unittest.TestSuite((suite1))


if __name__ == '__main__':
    # When this module is executed from the command-line, run all its tests
    unittest.main()
