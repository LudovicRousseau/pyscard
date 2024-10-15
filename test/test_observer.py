import unittest.mock

import pytest

import smartcard.Observer


def test_state_changes():
    """Verify that the "changed" state can be set and cleared."""

    # Base state
    observable = smartcard.Observer.Observable()
    assert not observable.hasChanged(), "Observable must not start in a changed state"

    # Set
    observable.setChanged()
    assert observable.hasChanged(), ".setChanged() must *set* the state"
    observable.setChanged()
    assert observable.hasChanged(), ".setChanged() must not *toggle* the state"

    # Clear
    observable.clearChanged()
    assert not observable.hasChanged(), ".clearChanged() must *clear* the state"
    observable.clearChanged()
    assert not observable.hasChanged(), ".clearChanged() must not *toggle* the state"


@pytest.mark.parametrize(
    "unbound_method",
    (
        # Observer management methods
        smartcard.Observer.Observable.addObserver,
        smartcard.Observer.Observable.countObservers,
        smartcard.Observer.Observable.deleteObserver,
        smartcard.Observer.Observable.deleteObservers,
        smartcard.Observer.Observable.notifyObservers,
        # State management methods
        smartcard.Observer.Observable.clearChanged,
        smartcard.Observer.Observable.hasChanged,
        smartcard.Observer.Observable.setChanged,
    ),
)
def test_synchronization(unbound_method):
    """Verify that all Observable methods are synchronized.

    The `.mutex` attribute is mocked and is confirmed to be acquired and released.

    The test implementation here doesn't necessarily make valid method calls;
    it relies on the knowledge that most Observable methods are decorated
    and that the lock is acquired before the underlying method is called
    (and thus, before Python realizes that required method parameters are unfilled
    and raises a TypeError).
    """

    mutex = unittest.mock.MagicMock()
    # Ensure the context manager protocol is functional.
    mutex.__enter__.return_value = mutex

    observable = smartcard.Observer.Observable()
    observable.mutex = mutex

    try:
        # Call the unbound Observable method, passing *observable* as `self`.
        unbound_method(observable)  # noqa
    except TypeError:
        # Ignore TypeErrors caused by missing mandatory method arguments.
        pass

    mutex.__enter__.assert_called_once()
    mutex.__exit__.assert_called_once()


def test_registered_observers_are_always_notified():
    """Verify all observers are notified, even if the observer list changes."""

    class JealousObserver(smartcard.Observer.Observer):
        update_count = 0

        def update(self, observable, _):
            # Try to prevent all other observers from receiving an update.
            for other_observer in observers - {self}:
                try:
                    observable.deleteObserver(other_observer)
                except ValueError:
                    pass

            # Track the number of times an update was received.
            JealousObserver.update_count += 1

    jealous_observer_count = 10
    observers = {JealousObserver() for _ in range(jealous_observer_count)}

    # Create a fair observable and notify the observers of a change.
    fair_observable = smartcard.Observer.Observable()
    [fair_observable.addObserver(observer) for observer in observers]
    fair_observable.setChanged()
    fair_observable.notifyObservers()

    # Confirm that the observers have all erased each other from the list of observers.
    assert fair_observable.countObservers() == 0

    # Confirm that the observers were all updated, despite their jealous efforts.
    assert JealousObserver.update_count == jealous_observer_count


def test_double_observer_additions():
    """Verify that an observer cannot be added twice."""

    observer = smartcard.Observer.Observer()
    observable = smartcard.Observer.Observable()
    observable.addObserver(observer)
    observable.addObserver(observer)

    assert observable.countObservers() == 1


def test_double_observer_removals():
    """Verify that an observer cannot be removed twice."""

    observer = smartcard.Observer.Observer()
    observable = smartcard.Observer.Observable()
    observable.addObserver(observer)
    observable.deleteObserver(observer)

    with pytest.raises(ValueError, match="x not in list"):
        observable.deleteObserver(observer)


def test_no_notifications_when_no_changes():
    """Verify that no notifications are sent when no changes are detected."""

    class Observer(smartcard.Observer.Observer):
        def update(self, *_, **__):
            raise RuntimeError("no updates were expected")

    observable = smartcard.Observer.Observable()
    observable.addObserver(Observer())
    # Attempt to send a notification when no changes have been made.
    # Nothing needs to be asserted here;
    # the lack of a RuntimeError during test execution demonstrates the test passed.
    observable.notifyObservers()


def test_default_observer_updates():
    """Call the default Observer.update() method.

    This test exists solely for the purposes of reaching 100% test coverage.
    It can be removed if Observer becomes an abstract base class.
    """

    observable = smartcard.Observer.Observable()
    assert smartcard.Observer.Observer().update(observable, "arg") is None
