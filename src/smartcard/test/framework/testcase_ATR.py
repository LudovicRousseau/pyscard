#! /usr/bin/env python3
"""Unit tests for testing that we have at least two cards for the test suite.

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

import sys
import unittest

sys.path += [".."]

try:
    from local_config import expectedATRs
except ImportError:
    print("execute test suite first to generate the local_config.py file")
    sys.exit()


class testcase_ATR(unittest.TestCase):
    """Test ATR configuration for test suite"""

    def testcase_ATRconfig(self):
        """ATRconfig"""
        # we have at list 2 readers (one is the simulator), e.g.
        # two potential ATRs
        self.assertTrue(len(expectedATRs) > 1)

        # we have at least two non empty ATRs
        count = 0
        for atr in expectedATRs:
            if atr:
                count += 1
        self.assertTrue(count > 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
