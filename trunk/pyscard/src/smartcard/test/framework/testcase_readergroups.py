#! /usr/bin/env python
"""Unit tests for smartcard.readers.ReaderGroups

This test case can be executed individually, or with all other test cases
thru testsuite_framework.py.

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

from smartcard.reader.ReaderGroups import readergroups
from smartcard.scard import resourceManager


if 'winscard' == resourceManager:

    class testcase_readergroups(unittest.TestCase):
        """Test smartcard framework readersgroups."""

        pinpadgroup = 'Pinpad$Readers'
        biogroup = 'Biometric$Readers'

        def testcase_readergroup_add(self):
            """tests groups=groups+[newgroups]"""

            # take a snapshot of current groups
            groupssnapshot = list(readergroups())
            groups = readergroups()

            # add pinpad group
            groups = groups + [self.pinpadgroup]
            self.assertEquals(groups, groupssnapshot + [self.pinpadgroup])

            # add pinpad a second time and biometric once
            groups = groups + [self.biogroup, self.pinpadgroup]
            self.assertEquals(groups, groupssnapshot + [self.pinpadgroup, self.biogroup])

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
            self.assertEquals(groups, groupssnapshot + [self.pinpadgroup])

            # add pinpad a second time and biometric once
            groups += [self.biogroup, self.pinpadgroup]
            self.assertEquals(groups, groupssnapshot + [self.pinpadgroup, self.biogroup])

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
            self.assertEquals(groups, groupssnapshot)
            self.assertEquals(zgroups, groupssnapshot + [self.pinpadgroup])
            self.assert_(isinstance(zgroups, type([])))
            self.assert_(isinstance(groups, type(readergroups())))

            # add pinpad a tiwce and biometric once
            zgroups = [self.pinpadgroup, self.biogroup, self.pinpadgroup] + groups
            self.assertEquals(groups, groupssnapshot)
            self.assertEquals(zgroups, groupssnapshot + [self.pinpadgroup, self.biogroup])
            self.assert_(isinstance(zgroups, type([])))
            self.assert_(isinstance(groups, type(readergroups())))

        def testcase_readergroup_append(self):
            """test groups.append(newgroups)"""

            # take a snapshot of current groups
            groupssnapshot = list(readergroups())
            groups = readergroups()

            # add pinpad group
            groups.append(self.pinpadgroup)
            self.assertEquals(groups, groupssnapshot + [self.pinpadgroup])

            # add pinpad a second time
            groups.append(self.pinpadgroup)
            self.assertEquals(groups, groupssnapshot + [self.pinpadgroup])

            # add biometric once
            groups.append(self.biogroup)
            self.assertEquals(groups, groupssnapshot + [self.pinpadgroup, self.biogroup])

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
            self.assertEquals(groups, groupssnapshot + [self.pinpadgroup])

            # add pinpad a second time
            groups.insert(1, self.pinpadgroup)
            self.assertEquals(groups, groupssnapshot + [self.pinpadgroup])

            # add biometric once
            groups.insert(1, self.biogroup)
            self.assertEquals(groups, groupssnapshot + [self.pinpadgroup, self.biogroup])

            # clean-up
            groups.remove(self.biogroup)
            groups.remove(self.pinpadgroup)

    def suite():
        suite1 = unittest.makeSuite(testcase_readergroups)
        return unittest.TestSuite((suite1))


if __name__ == '__main__':
    unittest.main()
