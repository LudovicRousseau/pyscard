#! /usr/bin/env python
"""Unit tests for ulist

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

from smartcard.ulist import ulist


class C(ulist):

    def __onadditem__(self, item):
        #print '+', item
        pass

    def __onremoveitem__(self, item):
        #print '-', item
        pass


class testcase_ulist(unittest.TestCase):
    """Test smartcard.ulist."""

    def testcase_ulist_init(self):
        """tests constructor"""

        c = C([1, 2, 3, 3, 4, 5, 5])
        self.assertEquals([1, 2, 3, 4, 5], c)

        c = C(['one', 'two', 'three', 'one'])
        self.assertEquals(['one', 'two', 'three'], c)

    def testcase_ulist_add(self):
        """tests l=l+other"""

        seed = [1, 2, 3]
        c = C(seed)
        self.assertEquals(seed, c)

        c = c + []
        self.assertEquals(seed, c)

        c = c + 4
        self.assertEquals(seed + [4], c)

        c = c + 4
        self.assertEquals(seed + [4], c)

        c = c + 'word'
        self.assertEquals(seed + [4] + ['word'], c)

        seed = ['one', 'two', 'three']
        c = C(seed)
        self.assertEquals(seed, c)

        c = c + ['four', 'five']
        self.assertEquals(seed + ['four', 'five'], c)

    def testcase_ulist_iadd(self):
        """tests l+=other"""

        seed = [1, 2, 3]
        c = C(seed)
        self.assertEquals(seed, c)

        c += []
        self.assertEquals(seed, c)

        c += 4
        self.assertEquals(seed + [4], c)

        c += 4
        self.assertEquals(seed + [4], c)

        c += [4, 3, 2, 1]
        self.assertEquals(seed + [4], c)

        c += 'word'
        self.assertEquals(seed + [4] + ['word'], c)

        seed = ['one', 'two', 'three']
        c = C(seed)
        self.assertEquals(seed, c)

        c += ['four', 'five']
        self.assertEquals(seed + ['four', 'five'], c)

    def testcase_ulist_radd(self):
        """tests l=other+l"""

        seed = [1, 2, 3]
        c = C(seed)
        self.assertEquals(seed, c)

        l = [] + c
        self.assertEquals(seed, l)

        l = [3] + c
        self.assertEquals(seed, c)
        self.assertEquals(seed, l)

        l = [3, 3, 4, 4] + c
        self.assertEquals(seed, c)
        self.assertEquals(seed + [4], l)

        l = [4] + ['word'] + c
        self.assertEquals(seed, c)
        self.assertEquals(seed + [4] + ['word'], l)

    def testcase_ulist_append(self):

        seed = [1, 2, 3]
        c = C(seed)

        c.append(4)
        self.assertEquals(seed + [4], c)

        c.append(4)
        self.assertEquals(seed + [4], c)

        c.append('word')
        self.assertEquals(seed + [4] + ['word'], c)

    def testcase_ulist_insert(self):

        seed = [1, 2, 3]
        c = C(seed)

        c.insert(0, 0)
        self.assertEquals([0] + seed, c)

        c.insert(1, 0)
        self.assertEquals([0] + seed, c)

    def testcase_ulist_pop(self):

        seed = [1, 2, 3]
        c = C(seed)

        c.pop()
        self.assertEquals(c, [1, 2])

        c.pop(1)
        self.assertEquals(c, [1])

    def testcase_ulist_remove(self):

        seed = [1, 2, 3]
        c = C(seed)

        c.remove(2)
        self.assertEquals(c, [1, 3])

        c.remove(1)
        self.assertEquals(c, [3])


def suite():
    suite1 = unittest.makeSuite(testcase_ulist)
    return unittest.TestSuite((suite1))


if __name__ == '__main__':
    unittest.main()
