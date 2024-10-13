from __future__ import annotations

import pytest

import smartcard.Synchronization


@pytest.mark.parametrize(
    "defined_methods, names, modified_methods",
    (
        # Nothing should be wrapped (str version)
        pytest.param(set(), "", set(), id="wrap nothing (str)"),
        pytest.param({"a"}, "", set(), id="wrap nothing (a, str)"),
        pytest.param({"a", "b"}, "", set(), id="wrap nothing (a+b, str)"),
        # Nothing should be wrapped (iterable version)
        pytest.param(set(), [], set(), id="wrap nothing (list)"),
        pytest.param({"a"}, [], set(), id="wrap nothing (a, list)"),
        pytest.param({"a", "b"}, [], set(), id="wrap nothing (a+b, list)"),
        # Everything should be wrapped
        pytest.param(set(), None, set(), id="wrap all"),
        pytest.param({"a"}, None, {"a"}, id="wrap all (a)"),
        pytest.param({"a", "b"}, None, {"a", "b"}, id="wrap all (a+b)"),
        # Only "a" should be wrapped (str version)
        pytest.param({"a"}, "a", {"a"}, id="wrap a only (a, str)"),
        pytest.param({"a", "b"}, "a", {"a"}, id="wrap a only (a+b, str)"),
        # Only "a" should be wrapped (list version)
        pytest.param({"a"}, ["a"], {"a"}, id="wrap a only (a, list)"),
        pytest.param({"a", "b"}, ["a"], {"a"}, id="wrap a only (a+b, list)"),
    ),
)
def test_synchronize(
    defined_methods: set[str],
    names: None | str | list[str],
    modified_methods: set[str],
):
    """Verify synchronize() wraps class methods as expected."""

    method_map = {method: lambda self: None for method in defined_methods}
    class_ = type("A", (object,), method_map)

    smartcard.Synchronization.synchronize(class_, names)

    for modified_method in modified_methods:
        assert getattr(class_, modified_method) is not method_map[modified_method]
    for unmodified_method in defined_methods - modified_methods:
        assert getattr(class_, unmodified_method) is method_map[unmodified_method]


def test_synchronization_reentrant_lock():
    """Verify Synchronization mutex locks are re-entrant by default."""

    class A(smartcard.Synchronization.Synchronization):
        def level_1(self):
            self.level_2()

        def level_2(self):
            return self

    smartcard.Synchronization.synchronize(A)

    instance = A()
    # If the synchronization lock is NOT re-entrant by default,
    # the test suite will hang when it reaches this line.
    instance.level_1()


def test_synchronization_wrapping():
    """Verify synchronized functions have correct names and docstrings."""

    class A(smartcard.Synchronization.Synchronization):
        def apple(self):
            """KEEP ME"""

    smartcard.Synchronization.synchronize(A)

    assert A.apple.__name__ == "apple"
    assert "KEEP ME" in A.apple.__doc__


def test_synchronization_kwargs():
    """Verify synchronized functions support arguments and keyword arguments."""

    class A(smartcard.Synchronization.Synchronization):
        def positional_only(self, positional, /):
            return positional

        def keyword_only(self, *, keyword):
            return keyword

    smartcard.Synchronization.synchronize(A)

    A().positional_only(True)
    A().keyword_only(keyword=True)
