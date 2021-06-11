#! /usr/bin/env python3
"""Unit tests for smartcard.ReaderMonitoring

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


import random
import threading
import time
import unittest

from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver

period = .1

# stats on virtual reader insertion/removal
insertedreaderstats = {}
removedreaderstats = {}

# the virtual list of readers
mutexvreaders = threading.RLock()
virtualreaders = []


def getReaders():
    '''Return virtual list of inserted readers.
    Replacement of smartcard.system.readers for testing purpose'''
    try:
        mutexvreaders.acquire()
        currentreaders = virtualreaders
    finally:
        mutexvreaders.release()
        readerEvent.set()
    return currentreaders

# an event to signal test threads to end
exitEvent = threading.Event()

# an event to ensure only one insertion/removal between getReaders() calls
readerEvent = threading.Event()
readerEvent.clear()

# test running time in seconds
RUNNING_TIME = 15

# the count of registered observers
OBS_COUNT = 100


class readerInsertionThread(threading.Thread):
    '''Simulate reader insertion every 2 to 4 periods.'''

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while not exitEvent.isSet():
            time.sleep(random.uniform(2 * period, 4 * period))
            readerEvent.wait()
            newreader = random.choice('abcdefghijklmnopqrstuvwxyz')
            try:
                mutexvreaders.acquire()
                if newreader not in virtualreaders:
                    virtualreaders.append(newreader)
                    if newreader in insertedreaderstats:
                        insertedreaderstats[newreader] += 1
                    else:
                        insertedreaderstats[newreader] = 1
            finally:
                readerEvent.clear()
                mutexvreaders.release()


class readerRemovalThread(threading.Thread):
    '''Simulate reader removal every 5 to 6 periods.'''

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while not exitEvent.isSet():
            time.sleep(random.uniform(5 * period, 6 * period))
            readerEvent.wait()
            try:
                mutexvreaders.acquire()
                if virtualreaders:
                    oldreader = random.choice(virtualreaders)
                    virtualreaders.remove(oldreader)
                    if oldreader in removedreaderstats:
                        removedreaderstats[oldreader] += 1
                    else:
                        removedreaderstats[oldreader] = 1
            finally:
                readerEvent.clear()
                mutexvreaders.release()


class countobserver(ReaderObserver):
    '''A simple reader observer that counts added/removed readers.'''

    def __init__(self, obsindex):
        self.obsindex = obsindex
        self.insertedreaderstats = {}
        self.removedreaderstats = {}
        self.countnotified = 0

    def update(self, observable, actions):
        (addedreaders, removedreaders) = actions
        self.countnotified += 1
        for newreader in addedreaders:
            if newreader in self.insertedreaderstats:
                self.insertedreaderstats[newreader] += 1
            else:
                self.insertedreaderstats[newreader] = 1
        for oldreader in removedreaders:
            if oldreader in self.removedreaderstats:
                self.removedreaderstats[oldreader] += 1
            else:
                self.removedreaderstats[oldreader] = 1


class testcase_readermonitorstress(unittest.TestCase):
    '''Test smartcard framework reader monitoring'''

    def testcase_readermonitorthread(self):

        # create thread that simulates reader insertion
        insertionthread = readerInsertionThread()

        # create thread that simulates reader removal
        removalthread = readerRemovalThread()

        readermonitor = ReaderMonitor(readerProc=getReaders, period=period)
        observers = []
        for i in range(0, OBS_COUNT):
            observer = countobserver(i)
            readermonitor.addObserver(observer)
            observers.append(observer)

        # signal threads to start
        insertionthread.start()
        removalthread.start()

        # let reader insertion/removal threads run for a while
        # then signal threads to end
        time.sleep(RUNNING_TIME)
        exitEvent.set()

        # wait until all threads ended
        removalthread.join()
        insertionthread.join()
        time.sleep(2 * period)

        for observer in observers:
            self.assertEqual(
                observer.insertedreaderstats, insertedreaderstats)
            self.assertEqual(
                observer.removedreaderstats, removedreaderstats)


def suite():
    suite1 = unittest.makeSuite(testcase_readermonitorthread)
    return unittest.TestSuite((suite1))


if __name__ == '__main__':
    unittest.main()
