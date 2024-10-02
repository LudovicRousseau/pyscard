import pytest

import smartcard.ulist


def test_demonstrate_ulist_cannot_be_instantiated():
    """ulist() cannot be instantiated without an argument."""

    with pytest.raises(TypeError, match="'NoneType' object is not iterable"):
        smartcard.ulist.ulist()


@pytest.mark.xfail(reason="order should be ['x', 1, 2] not [1, 2, 'x']", strict=True)
def test_demonstrate_order_is_not_respected():
    """Order is not strictly respected."""

    instance = smartcard.ulist.ulist([1, 2])
    new_instance = ["x"] + instance
    assert new_instance == ["x", 1, 2]


@pytest.mark.xfail(reason="not all list methods are overwritten", strict=True)
def test_demonstrate_non_unique_behavior():
    """ulist.extend() breaks uniqueness guarantees."""

    instance = smartcard.ulist.ulist([1, 2])
    instance.extend([1, 2, 3])
    assert instance == [1, 2]  # actually, it's [1, 2, 1, 2, 3]


def test_ulist_methods():
    """This broadly tests the ulist implementation.

    It can be removed when ulist is removed.
    """

    smartcard.ulist.ulist([])
    smartcard.ulist.ulist([1])
    smartcard.ulist.ulist([1, 1])
    instance = smartcard.ulist.ulist([1])
    original_id = id(instance)
    assert instance
    assert len(instance) == 1
    assert instance == [1]
    assert id(instance) == original_id

    instance.append(1)
    assert instance
    assert len(instance) == 1
    assert instance == [1]
    assert id(instance) == original_id

    instance.append(2)
    assert instance
    assert len(instance) == 2
    assert instance == [1, 2]
    assert id(instance) == original_id

    new_instance = instance + [3]
    assert new_instance is not instance
    assert new_instance == [1, 2, 3]
    assert instance == [1, 2]
    assert id(instance) == original_id

    new_instance = instance + [1, 2]
    assert new_instance is not instance
    assert new_instance == [1, 2]
    assert instance == [1, 2]
    assert id(instance) == original_id

    new_instance = [1, 2] + instance
    assert new_instance is not instance
    assert new_instance == [1, 2]
    assert instance == [1, 2]
    assert id(instance) == original_id

    instance += 2
    assert instance == [1, 2]
    assert id(instance) == original_id

    instance.insert(0, 0)
    assert len(instance) == 3
    assert instance == [0, 1, 2]

    instance.insert(10_000, 0)
    assert len(instance) == 3
    assert instance == [0, 1, 2]

    value = instance.pop()
    assert value == 2
    assert instance == [0, 1]
    value = instance.pop(0)
    assert value == 0
    assert instance == [1]
    instance.pop()

    instance.append(0)
    instance.remove(0)
    with pytest.raises(ValueError):
        instance.remove(0)

    my_pristine_list = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    instance += my_pristine_list
    assert my_pristine_list == [0, 1, 2, 0, 1, 2, 0, 1, 2]
