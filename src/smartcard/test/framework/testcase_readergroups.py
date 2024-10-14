#! /usr/bin/env python3
"""Unit tests for smartcard.readers.ReaderGroups

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

import unittest

from smartcard.scard import resourceManager
from smartcard.System import readergroups

if "winscard" == resourceManager:

    class testcase_readergroups(unittest.TestCase):
        """Test smartcard framework readersgroups."""

        pinpadgroup = "Pinpad$Readers"
        biogroup = "Biometric$Readers"

        def testcase_readergroup_add(self):
            """tests groups=groups+[newgroups]"""

            # take a snapshot of current groups
            groupssnapshot = list(readergroups())
            groups = readergroups()

            # add pinpad group
            groups = groups + [self.pinpadgroup]
            self.assertEqual(groups, groupssnapshot + [self.pinpadgroup])

            # add pinpad a second time and biometric once
            groups = groups + [self.biogroup, self.pinpadgroup]
            self.assertEqual(groups, groupssnapshot + [self.pinpadgroup, self.biogroup])

            # clean-up
            groups.remove(self.biogroup)
            groups.remove(self.pinpadgroup)

        def testcase_readergroup_iadd(self):
            """test groups+=[newgroups]"""

            # take a snapshot of current groups
            groupssnapshot = list(readergroups())
            groups = readergroups()

            # add pinpad group
            groups += [self.pinpadgroup]
            self.assertEqual(groups, groupssnapshot + [self.pinpadgroup])

            # add pinpad a second time and biometric once
            groups += [self.biogroup, self.pinpadgroup]
            self.assertEqual(groups, groupssnapshot + [self.pinpadgroup, self.biogroup])

            # clean-up
            groups.remove(self.biogroup)
            groups.remove(self.pinpadgroup)

        def testcase_readergroup_radd(self):
            """test groups=[newgroups]+groups"""

            # take a snapshot of current groups
            groupssnapshot = list(readergroups())
            groups = readergroups()

            # add pinpad group
            zgroups = [self.pinpadgroup] + groups
            self.assertEqual(groups, groupssnapshot)
            self.assertEqual(zgroups, groupssnapshot + [self.pinpadgroup])
            self.assertTrue(isinstance(zgroups, list))
            self.assertTrue(isinstance(groups, type(readergroups())))

            # add pinpad a tiwce and biometric once
            zgroups = [self.pinpadgroup, self.biogroup, self.pinpadgroup] + groups
            self.assertEqual(groups, groupssnapshot)
            self.assertEqual(
                zgroups, groupssnapshot + [self.pinpadgroup, self.biogroup]
            )
            self.assertTrue(isinstance(zgroups, list))
            self.assertTrue(isinstance(groups, type(readergroups())))

        def testcase_readergroup_append(self):
            """test groups.append(newgroups)"""

            # take a snapshot of current groups
            groupssnapshot = list(readergroups())
            groups = readergroups()

            # add pinpad group
            groups.append(self.pinpadgroup)
            self.assertEqual(groups, groupssnapshot + [self.pinpadgroup])

            # add pinpad a second time
            groups.append(self.pinpadgroup)
            self.assertEqual(groups, groupssnapshot + [self.pinpadgroup])

            # add biometric once
            groups.append(self.biogroup)
            self.assertEqual(groups, groupssnapshot + [self.pinpadgroup, self.biogroup])

            # clean-up
            groups.remove(self.biogroup)
            groups.remove(self.pinpadgroup)

        def testcase_readergroup_insert(self):
            """test groups.insert(i,newgroups)"""

            # take a snapshot of current groups
            groupssnapshot = list(readergroups())
            groups = readergroups()

            # add pinpad group
            groups.insert(0, self.pinpadgroup)
            self.assertEqual(groups, groupssnapshot + [self.pinpadgroup])

            # add pinpad a second time
            groups.insert(1, self.pinpadgroup)
            self.assertEqual(groups, groupssnapshot + [self.pinpadgroup])

            # add biometric once
            groups.insert(1, self.biogroup)
            self.assertEqual(groups, groupssnapshot + [self.pinpadgroup, self.biogroup])

            # clean-up
            groups.remove(self.biogroup)
            groups.remove(self.pinpadgroup)


if __name__ == "__main__":
    unittest.main()
