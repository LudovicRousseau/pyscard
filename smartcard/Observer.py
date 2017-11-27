"""
from Thinking in Python, Bruce Eckel
http://python-3-patterns-idioms-test.readthedocs.org/en/latest/Observer.html

(c) Copyright 2008, Creative Commons Attribution-Share Alike 3.0.

Class support for "observer" pattern.

The observer class is the base class
for all smartcard package observers.

Known subclasses: L{smartcard.ReaderObserver}

"""

from smartcard.Synchronization import *


class Observer(object):

    def update(observable, arg):
        '''Called when the observed object is
        modified. You call an Observable object's
        notifyObservers method to notify all the
        object's observers of the change.'''
        pass


class Observable(Synchronization):

    def __init__(self):
        self.obs = []
        self.changed = 0
        Synchronization.__init__(self)

    def addObserver(self, observer):
        if observer not in self.obs:
            self.obs.append(observer)

    def deleteObserver(self, observer):
        self.obs.remove(observer)

    def notifyObservers(self, arg=None):
        '''If 'changed' indicates that this object
        has changed, notify all its observers, then
        call clearChanged(). Each observer has its
        update() called with two arguments: this
        observable object and the generic 'arg'.'''

        self.mutex.acquire()
        try:
            if not self.changed:
                    return
            # Make a local copy in case of synchronous
            # additions of observers:
            localArray = self.obs[:]
            self.clearChanged()
        finally:
            self.mutex.release()
        # Update observers
        for observer in localArray:
            observer.update(self, arg)

    def deleteObservers(self):
            self.obs = []

    def setChanged(self):
            self.changed = 1

    def clearChanged(self):
            self.changed = 0

    def hasChanged(self):
            return self.changed

    def countObservers(self):
            return len(self.obs)


synchronize(Observable,
            "addObserver deleteObserver deleteObservers " +
            "setChanged clearChanged hasChanged " +
            "countObservers")
