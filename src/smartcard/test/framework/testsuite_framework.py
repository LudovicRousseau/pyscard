#! /usr/bin/env python3
"""Unit test suite for smartcard python framework.

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

# so that we can locate configcheck
sys.path += [".."]
import configcheck


def suite():
    """suite"""
    modules_to_test = (
        "testcase_ATR",
        "testcase_Card",
        "testcase_CardConnection",
        "testcase_CardMonitor",
        "testcase_CardRequest",
        "testcase_CardService",
        "testcase_CardType",
        "testcase_CAtr",
        "testcase_ErrorChecking",
        "testcase_ExclusiveCardConnection",
        "testcase_readers",
        "testcase_readergroups",
        "testcase_readermonitor",
        "testcase_readermonitorstress",
        "testcase_ulist",
        "testcase_utils",
    )
    testsuite_framework = unittest.TestSuite()
    for module in map(__import__, modules_to_test):
        testsuite_framework.addTest(unittest.TestLoader().loadTestsFromModule(module))
    return testsuite_framework


if __name__ == "__main__":
    configcheck.checklocalconfig()
    # set verbosity=2 to get more details
    unittest.main(defaultTest="suite", verbosity=2)
