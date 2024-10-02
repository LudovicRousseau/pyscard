import pytest

import smartcard.reader.ReaderGroups


@pytest.fixture(autouse=True)
def reset_reader_groups():
    """Reader group instances must be reset at the beginning of each test."""

    smartcard.reader.ReaderGroups.readergroups.instance = None
    yield
