"""
from Thinking in Python, Bruce Eckel
http://mindview.net/Books/TIPython

Simple emulation of Java's 'synchronized'
keyword, from Peter Norvig.
"""

from threading import RLock


def synchronized(method):

    def f(*args):
        self = args[0]
        self.mutex.acquire()
        # print method.__name__, 'acquired'
        try:
            return apply(method, args)
        finally:
            self.mutex.release()
            # print method.__name__, 'released'
    return f


def synchronize(klass, names=None):
    """Synchronize methods in the given class.
    Only synchronize the methods whose names are
    given, or all methods if names=None."""
    if type(names) == type(''):
            names = names.split()
    for (name, val) in klass.__dict__.items():
        if callable(val) and name != '__init__' and \
            (names == None or name in names):
                # print "synchronizing", name
                klass.__dict__[name] = synchronized(val)


class Synchronization:
    # You can create your own self.mutex, or inherit from this class:

    def __init__(self):
        self.mutex = RLock()
