"""
from Thinking in Python, Bruce Eckel
https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Observer.html

(c) Copyright 2008, Creative Commons Attribution-Share Alike 3.0.

Class support for "observer" pattern.

The observer class is the base class
for all smartcard package observers.
"""

from __future__ import annotations

import typing

from smartcard.Synchronization import Synchronization, synchronize


class Observer:
    def update(self, observable: Observable, arg: typing.Any) -> None:
        """Called when the observed object is
        modified. You call an Observable object's
        notifyObservers method to notify all the
        object's observers of the change."""
        pass


class Observable(Synchronization):
    def __init__(self) -> None:
        super().__init__()
        self.obs: list[Observer] = []
        self.changed = 0

    def addObserver(self, observer: Observer) -> None:
        if observer not in self.obs:
            self.obs.append(observer)

    def deleteObserver(self, observer: Observer) -> None:
        self.obs.remove(observer)

    def notifyObservers(self, arg: typing.Any = None) -> None:
        """If 'changed' indicates that this object
        has changed, notify all its observers, then
        call clearChanged(). Each observer has its
        update() called with two arguments: this
        observable object and the generic 'arg'."""

        with self.mutex:
            if not self.changed:
                return
            # Make a copy of the observer list.
            observers = self.obs.copy()
            self.changed = 0

        # Update observers
        for observer in observers:
            observer.update(self, arg)

    def deleteObservers(self) -> None:
        self.obs = []

    def setChanged(self) -> None:
        self.changed = 1

    def clearChanged(self) -> None:
        self.changed = 0

    def hasChanged(self) -> int:
        return self.changed

    def countObservers(self) -> int:
        return len(self.obs)


synchronize(
    Observable,
    "addObserver deleteObserver deleteObservers "
    + "setChanged clearChanged hasChanged "
    + "countObservers",
)
