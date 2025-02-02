import pytest

import smartcard.reader.ReaderGroups
import smartcard.ulist


def test_reader_groups_acts_like_a_singleton():
    """Verify that the target class *acts* like a singleton."""

    instance_1 = smartcard.reader.ReaderGroups.readergroups()
    instance_2 = smartcard.reader.ReaderGroups.readergroups()
    assert instance_1.instance is instance_2.instance


def test_reader_groups_method_calls():
    reader_group = smartcard.reader.ReaderGroups.readergroups()
    assert len(reader_group.instance) == 0, "No reader groups should be pre-defined"

    list.append(reader_group.instance, "a")
    assert len(reader_group.instance) == 1, "Unable to add a reader group"

    reader_group.addreadergroup("a")
    assert len(reader_group.instance) == 1, "Reader groups must be unique"

    with pytest.raises(smartcard.reader.ReaderGroups.BadReaderGroupException):
        reader_group.addreadergroup(1)
    with pytest.raises(smartcard.reader.ReaderGroups.BadReaderGroupException):
        reader_group.removereadergroup(1)

    # .__iter__()
    assert len(list(reader_group.instance)) == 1

    # No-op calls
    reader_group.addreadertogroup("no-op", "bogus")
    reader_group.removereaderfromgroup("no-op", "bogus")

    assert list.pop(reader_group.instance) == "a"
    assert len(list(reader_group.instance)) == 0


# ------------------------------------------------------------------------------------
# The tests below this line demonstrate serious behavioral problems with readergroups.


@pytest.mark.xfail(reason="readergroups is not actually a singleton", strict=True)
def test_reader_groups_is_a_singleton():
    """Verify that readergroups is a singleton."""

    instance_1 = smartcard.reader.ReaderGroups.readergroups()
    instance_2 = smartcard.reader.ReaderGroups.readergroups()
    assert instance_1 is instance_2


@pytest.mark.xfail(reason="initlist parameters may be silently ignored", strict=True)
def test_demonstrate_initlist_values_may_be_silently_ignored():
    """Demonstrate that `initlist` parameters may be silently ignored."""

    smartcard.reader.ReaderGroups.readergroups(["a"])
    reader_group = smartcard.reader.ReaderGroups.readergroups(["b"])
    assert "b" in reader_group.instance


def test_demonstrate_adding_is_impossible():
    """Demonstrate that `.addreadergroup()` cannot be called."""

    reader_group = smartcard.reader.ReaderGroups.readergroups()
    with pytest.raises(RecursionError, match="maximum recursion depth exceeded"):
        reader_group.addreadergroup("a")


def test_demonstrate_removing_is_impossible():
    """Demonstrate that `.removereadergroup()` cannot be called.

    `.removereadergroup()` recurses twice.
    It successfully removes the value, then fails to find it the second time.
    """

    reader_group = smartcard.reader.ReaderGroups.readergroups()
    list.append(reader_group.instance, "a")
    assert reader_group.instance == ["a"]
    with pytest.raises(ValueError, match="x not in list"):
        reader_group.removereadergroup("a")
    assert reader_group.instance == []


def test_demonstrate_getting_is_impossible():
    """Demonstrate that `.getreadergroups()` returns hard-coded values."""

    reader_group = smartcard.reader.ReaderGroups.readergroups()
    list.append(reader_group.instance, "a")
    assert reader_group.instance == ["a"]
    assert reader_group.getreadergroups() == []
    assert list.pop(reader_group.instance) == "a"
    assert len(list(reader_group.instance)) == 0
