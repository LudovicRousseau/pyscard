#! /usr/bin/env python3
"""Unit tests for smartcard.ReaderMonitoring

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
import threading
import time
import unittest

sys.path += [".."]

try:
    from local_config import expectedReaders
except ImportError:
    print("execute test suite first to generate the local_config.py file")
    sys.exit()


from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver


# a simple reader observer that prints added/removed readers
class printobserver(ReaderObserver):
    """observer"""

    def __init__(self, obsindex, testcase):
        self.obsindex = obsindex
        self.testcase = testcase

    def update(self, observable, handlers):
        (addedreaders, removedreaders) = handlers
        foundreaders = {}
        self.testcase.assertEqual(removedreaders, [])
        for reader in addedreaders:
            foundreaders[str(reader)] = 1
        if foundreaders:
            for reader in expectedReaders:
                self.testcase.assertTrue(reader in foundreaders)


class testthread(threading.Thread):
    """thread"""

    def __init__(self, obsindex, testcase):
        threading.Thread.__init__(self)
        self.obsindex = obsindex
        self.testcase = testcase
        self.readermonitor = ReaderMonitor()
        self.observer = None

    def run(self):
        # create and register observer
        self.observer = printobserver(self.obsindex, self.testcase)
        self.readermonitor.addObserver(self.observer)
        time.sleep(1)
        self.readermonitor.deleteObserver(self.observer)


class testcase_readermonitor(unittest.TestCase):
    """Test smartcard framework reader monitoring methods"""

    def testcase_readermonitorthread(self):
        """readermonitor thread"""
        threads = []
        for i in range(0, 4):
            t = testthread(i, self)
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()


if __name__ == "__main__":
    unittest.main(verbosity=1)
