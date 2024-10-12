#! /usr/bin/env python3
"""Unit test suite for scard python module.

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
        "testcase_getatr",
        "testcase_getattrib",
        "testcase_geterrormessage",
        "testcase_listcards",
        "testcase_locatecards",
        "testcase_readergroups",
        "testcase_returncodes",
        "testcase_transaction",
    )
    testsuite_scard = unittest.TestSuite()
    for module in map(__import__, modules_to_test):
        testsuite_scard.addTest(unittest.TestLoader().loadTestsFromModule(module))
    return testsuite_scard


if __name__ == "__main__":
    configcheck.checklocalconfig()
    unittest.main(defaultTest="suite", verbosity=1)
