#! /usr/bin/env python3
"""Unit tests for smartcard.pcsc.readers

This test case can be executed individually, or with all other test cases
thru testsuite_framework.py.

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


# import local_config for reader/card configuration
# configcheck.py is generating local_config.py in
# the test suite.
import sys
import unittest

sys.path += [".."]

try:
    from local_config import (
        expectedATRinReader,
        expectedATRs,
        expectedReaderGroups,
        expectedReaders,
    )
except ImportError:
    print("execute test suite first to generate the local_config.py file")
    sys.exit()


from smartcard.pcsc.PCSCReader import PCSCReader
from smartcard.pcsc.PCSCReaderGroups import PCSCReaderGroups
from smartcard.scard import resourceManager

if "winscard" == resourceManager:

    class testcase_readergroups(unittest.TestCase):
        """Test smartcard framework readers factory methods"""

        def setUp(self):
            groups = PCSCReaderGroups().instance
            groups.remove("Pinpad$Readers")
            groups.remove("Biometric$Readers")

        def testcase_add(self):
            """Test for groups=groups+newgroups"""
            groupssnapshot = list(PCSCReaderGroups().instance)
            groups = PCSCReaderGroups().instance
            newgroup = "Pinpad$Readers"
            groups = groups + newgroup
            self.assertEqual(groups, groupssnapshot + [newgroup])
            groups.remove(newgroup)

        def testcase_addlist(self):
            """Test for groups=groups+[newgroups]"""
            groupssnapshot = list(PCSCReaderGroups().instance)
            groups = PCSCReaderGroups().instance
            newgroups = ["Pinpad$Readers", "Biometric$Readers"]
            groups = groups + newgroups
            self.assertEqual(groups, groupssnapshot + newgroups)
            for group in newgroups:
                groups.remove(group)

        def testcase_iadd(self):
            """Test for groups+=newgroup"""
            groupssnapshot = list(PCSCReaderGroups().instance)
            groups = PCSCReaderGroups().instance
            newgroup = "Pinpad$Readers"
            groups += newgroup
            self.assertEqual(groups, groupssnapshot + [newgroup])
            groups.remove(newgroup)

        def testcase_iaddlist(self):
            """Test for groups+=[newgroups]"""
            groupssnapshot = list(PCSCReaderGroups().instance)
            groups = PCSCReaderGroups().instance
            newgroups = ["Pinpad$Readers", "Biometric$Readers"]
            groups += newgroups
            self.assertEqual(groups, groupssnapshot + newgroups)
            for group in newgroups:
                groups.remove(group)

        def testcase_append(self):
            """Test for groups.append(newgroup)"""
            groupssnapshot = list(PCSCReaderGroups().instance)
            groups = PCSCReaderGroups().instance
            newgroup = "Pinpad$Readers"
            groups.append(newgroup)
            self.assertEqual(groups, groupssnapshot + [newgroup])
            groups.remove(newgroup)

        def testcase_insert(self):
            """Test for groups.insert(newgroup)"""
            groupssnapshot = list(PCSCReaderGroups().instance)
            groups = PCSCReaderGroups().instance
            newgroup = "Pinpad$Readers"
            groups.insert(0, newgroup)
            self.assertEqual(groups, [newgroup] + groupssnapshot)
            groups.remove(newgroup)

        def testcase_removereadergroup_pop(self):
            """Test for groups.pop()"""
            groupssnapshot = list(PCSCReaderGroups().instance)
            groups = PCSCReaderGroups().instance
            newgroup = "Pinpad$Readers"
            groups.insert(0, newgroup)
            self.assertEqual(groups, [newgroup] + groupssnapshot)
            groups.pop(0)
            self.assertEqual(groups, groupssnapshot)

        def testcase_addreadertogroup(self):
            """Test for adding readers to group"""
            groups = PCSCReaderGroups().instance
            newgroup = "Pinpad$Readers"
            groups.insert(0, newgroup)
            for r in PCSCReader.readers("SCard$DefaultReaders"):
                r.addtoreadergroup(newgroup)
            self.assertEqual(
                PCSCReader.readers("SCard$DefaultReaders"), PCSCReader.readers(newgroup)
            )
            groups.pop(0)
            self.assertEqual([], PCSCReader.readers(newgroup))

        def testcase_removereaderfromgroup(self):
            """Test for removing readers from group"""
            groups = PCSCReaderGroups().instance
            newgroup = "Pinpad$Readers"
            groups.insert(0, newgroup)
            for r in PCSCReader.readers("SCard$DefaultReaders"):
                r.addtoreadergroup(newgroup)
            self.assertEqual(
                PCSCReader.readers("SCard$DefaultReaders"), PCSCReader.readers(newgroup)
            )
            for r in PCSCReader.readers("SCard$DefaultReaders"):
                r.removefromreadergroup(newgroup)
            self.assertEqual([], PCSCReader.readers(newgroup))
            groups.pop(0)
            self.assertEqual([], PCSCReader.readers(newgroup))

    def suite():
        suite1 = unittest.defaultTestLoader.loadTestsFromTestCase(testcase_readergroups)
        return unittest.TestSuite(suite1)

else:
    print("These tests are for Windows only")

if __name__ == "__main__":
    unittest.main()
