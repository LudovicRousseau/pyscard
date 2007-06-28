"""Smart card reader monitoring classes.

ReaderObserver is a base class for objects that are to be notified
upon smartcard reader insertion/removal.

ReaderMonitor is a singleton object notifying registered ReaderObservers
upon reader insertion/removal.

__author__ = "http://www.gemalto.com"

Copyright 2001-2007 gemalto
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

from sys import exc_info
from threading import Thread, Event
from time import sleep

from smartcard.System import readers
from smartcard.Exceptions import ListReadersException
from smartcard.Observer import Observer
from smartcard.Observer import Observable

from smartcard.Synchronization import *

_START_ON_DEMAND_=False

# ReaderObserver interface
class ReaderObserver(Observer):
    """
    ReaderObserver is a base abstract class for objects that are to be notified
    upon smartcard reader insertion/removal.
    """
    def __init__(self):
        pass
    def update( self, observable, (addedreaders, removedreaders) ):
        """Called upon reader insertion/removal.

        observable:
        addedreaders: list of added readers causing notification
        removedreaders: list of removed readers causing notification
        """
        pass

class ReaderMonitor:
    """Class that monitors reader insertion/removal.
    and notify observers

    note: a reader monitoring thread will be running
    as long as the reader monitor has observers, or ReaderMonitor.stop()
    is called. Do not forget to delete all your observer by
    calling deleteObserver, or your program will run forever...

    Not that we use the singleton pattern from Thinking in Python
    Bruce Eckel, http://mindview.net/Books/TIPython to make sure
    there is only one ReaderMonitor.
    """

    class __ReaderMonitorSingleton( Observable ):
        """The real reader monitor class.

        A single instance of this class is created
        by the public ReaderMonitor class.
        """
        def __init__(self):
            Observable.__init__(self)
            if _START_ON_DEMAND_:
                self.rmthread=None
            else:
                self.rmthread = ReaderMonitoringThread( self )

        def addObserver(self, observer):
            """Add an observer.

            We only start the reader monitoring thread when
            there are observers.
            """
            Observable.addObserver( self, observer )
            if _START_ON_DEMAND_:
                if self.countObservers()>0 and self.rmthread==None:
                    self.rmthread = ReaderMonitoringThread( self )
            else:
                observer.update( self, (self.rmthread.readers, [] ) )

        def deleteObserver(self, observer):
            """Remove an observer.

            We stop the reader monitoring thread when there
            are no more observers.
            """
            Observable.deleteObserver( self, observer )
            if _START_ON_DEMAND_:
                if self.countObservers()==0:
                    if self.rmthread!=None:
                        self.rmthread.stop()
                        self.rmthread=None

        def __str__( self ):
            return 'ReaderMonitor'

    # the singleton
    instance = None

    def __init__(self):
        if not ReaderMonitor.instance:
            ReaderMonitor.instance = ReaderMonitor.__ReaderMonitorSingleton()

    def __getattr__(self, name):
        return getattr(self.instance, name)

class ReaderMonitoringThread:
    """Reader insertion thread.
    This thread polls for pcsc reader insertion, since no
    reader insertion event is available in pcsc.
    """

    class __ReaderMonitoringThreadSingleton( Thread ):
        """The real reader monitoring thread class.

        A single instance of this class is created
        by the public ReaderMonitoringThread class.
        """
        def __init__(self, observable):
            Thread.__init__(self)
            self.observable=observable
            self.stopEvent = Event()
            self.stopEvent.clear()
            self.readers = []
            self.setDaemon(True)

        # the actual monitoring thread
        def run(self):
            """Runs until stopEvent is notified, and notify
            observers of all reader insertion/removal.
            """
            while self.stopEvent.isSet()!=1:
                try:
                    currentreaders = readers()

                    addedreaders=[]
                    for reader in currentreaders:
                        if not self.readers.__contains__( reader ):
                            addedreaders.append( reader )

                    removedreaders=[]
                    for reader in self.readers:
                        if not currentreaders.__contains__( reader ):
                            removedreaders.append( reader )

                    if addedreaders!=[] or removedreaders!=[]:
                        self.readers=currentreaders
                        self.observable.setChanged()
                        self.observable.notifyObservers( (addedreaders, removedreaders) )

                # when ReaderMonitoringThread.__del__() is invoked in response to shutdown,
                # e.g., when execution of the program is done, other globals referenced
                # by the __del__() method may already have been deleted.
                # this causes ReaderMonitoringThread.run() to except with a TypeError
                except TypeError:
                    pass

                except:
                    import sys
                    print sys.exc_info()[1]
                    print sys.exc_info()[2]
                    print sys.exc_info()[0]

                # don't poll too much
                sleep(1)


        # stop the thread by signaling stopEvent
        def stop(self):
            self.stopEvent.set()

    # the singleton
    instance = None

    def __init__(self, observable):
        if not ReaderMonitoringThread.instance:
            ReaderMonitoringThread.instance = ReaderMonitoringThread.__ReaderMonitoringThreadSingleton( observable )
            ReaderMonitoringThread.instance.start()


    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __del__(self):
        if ReaderMonitoringThread.instance!=None:
            ReaderMonitoringThread.instance.stop()
            ReaderMonitoringThread.instance = None


if __name__ == "__main__":
    from smartcard.ReaderMonitoring import ReaderMonitor
    print 'insert or remove readers in the next 10 seconds'

    # a simple reader observer that prints added/removed readers
    class printobserver( ReaderObserver ):
        def __init__( self, obsindex ):
            self.obsindex=obsindex

        def update( self, observable, (addedreaders, removedreaders) ):
            print "%d - added:   " % self.obsindex, addedreaders
            print "%d - removed: " % self.obsindex, removedreaders

    class testthread( Thread ):
        def __init__(self, obsindex ):
            Thread.__init__(self)
            self.readermonitor = ReaderMonitor()
            self.obsindex = obsindex
            self.observer=None

        def run(self):
            # create and register observer
            self.observer = printobserver( self.obsindex )
            self.readermonitor.addObserver(self.observer)
            sleep(10)
            self.readermonitor.deleteObserver(self.observer)

    t1 = testthread(1)
    t2 = testthread(2)
    t1.start()
    t2.start()


