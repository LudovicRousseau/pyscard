#! /usr/bin/env python3
"""Unit tests for smartcard.readers.

This test case can be executed individually, or with all other test cases
thru testsuite_framework.py.

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


import unittest

# import local_config for reader/card configuration
# configcheck.py is generating local_config.py in
# the test suite.
import sys
sys.path += ['..']

try:
    from local_config import expectedATRs, expectedReaders
    from local_config import expectedReaderGroups, expectedATRinReader
except ImportError:
    print('execute test suite first to generate the local_config.py file')
    sys.exit()


from smartcard.System import readers, readergroups
from smartcard import listReaders
from smartcard.scard import resourceManager


class testcase_readers(unittest.TestCase):
    """Test smartcard framework readers factory methods"""

    def testcase_enoughreaders(self):
        self.assertTrue(len(readers()) > 1)

    def testcase_readers(self):
        foundreaders = {}
        for reader in readers():
            foundreaders[str(reader)] = 1
        for reader in expectedReaders:
            self.assertTrue(reader in foundreaders)

    def testcase_hashreaders(self):
        foundreaders = {}
        for reader in readers():
            foundreaders[reader] = 1
        for reader in list(foundreaders.keys()):
            self.assertTrue(reader in readers())

    def testcase_legacyreaders(self):
        foundreaders = {}
        for reader in listReaders():
            foundreaders[reader] = 1
        for reader in expectedReaders:
            self.assertTrue(reader in foundreaders)

    def testcase_readers_in_readergroup(self):
        foundreaders = {}
        for reader in readers(['SCard$DefaultReaders']):
            foundreaders[str(reader)] = 1
        for reader in expectedReaders:
            self.assertTrue(reader in foundreaders)

    def testcase_readers_in_readergroup_empty(self):
        foundreaders = {}
        for reader in readers([]):
            foundreaders[str(reader)] = 1
        for reader in expectedReaders:
            self.assertTrue(reader in foundreaders)

    if 'winscard' == resourceManager:

        def testcase_readers_in_readergroup_nonexistent(self):
            foundreaders = {}
            for reader in readers(['dummy$group']):
                foundreaders[reader] = 1
            for reader in expectedReaders:
                self.assertTrue(not reader in foundreaders)
            self.assertEqual(0, len(foundreaders))

    def testcase_readergroups(self):
        foundreadergroups = {}
        for readergroup in readergroups():
            foundreadergroups[readergroup] = 1
        for readergroup in expectedReaderGroups:
            self.assertTrue(readergroup in foundreadergroups)


def suite():
    suite1 = unittest.makeSuite(testcase_readers)
    return unittest.TestSuite((suite1))


if __name__ == '__main__':
    unittest.main()
