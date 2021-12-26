# -*- coding: utf-8 -*-

# to execute:
# $ cd test
# $ python -m unittest

import unittest
from smartcard.pcsc.PCSCExceptions import *
from smartcard.scard import *
from distutils.util import get_platform


class TestUtil(unittest.TestCase):

    def test_ListReadersException(self):
        exc = ListReadersException(0)
        self.assertEqual(exc.hresult, 0)
        text = str(exc)
        if get_platform().startswith('win'):
            expected = "Failed to list readers: The operation completed successfully.  (0x00000000)"
        else:
            expected = "Failed to list readers: Command successful. (0x00000000)"
        self.assertEqual(text, expected)

        exc = ListReadersException(0x42)
        self.assertEqual(exc.hresult, 0x42)
        text = str(exc)
        if get_platform().startswith('win'):
            expected = "Failed to list readers: The network resource type is not correct.  (0x00000042)"
        else:
            expected = "Failed to list readers: Unknown error: 0x00000042 (0x00000042)"
        macos_bug_expected = expected.replace("Unknown", "Unkown")
        self.assertIn(text, [expected, macos_bug_expected])

        exc = ListReadersException(SCARD_S_SUCCESS)
        self.assertEqual(exc.hresult, 0)

        exc = ListReadersException(SCARD_E_NO_SERVICE)
        self.assertEqual(exc.hresult, SCARD_E_NO_SERVICE)
        text = str(exc)
        if get_platform().startswith('win'):
            expected = "Failed to list readers: The Smart Card Resource Manager is not running.  (0x8010001D)"
        else:
            expected = "Failed to list readers: Service not available. (0x8010001D)"
        self.assertEqual(text, expected)

    def test_EstablishContextException(self):
        exc = EstablishContextException(SCARD_E_NO_SERVICE)
        self.assertEqual(exc.hresult, SCARD_E_NO_SERVICE)
        text = str(exc)
        if get_platform().startswith('win'):
            expected = "Failed to establish context: The Smart Card Resource Manager is not running.  (0x8010001D)"
        else:
            expected = "Failed to establish context: Service not available. (0x8010001D)"
        self.assertEqual(text, expected)

    def test_IntroduceReaderException(self):
        exc = IntroduceReaderException(SCARD_E_DUPLICATE_READER, "foobar")
        self.assertEqual(exc.hresult, SCARD_E_DUPLICATE_READER)
        text = str(exc)
        if get_platform().startswith('win'):
            expected = "Failed to introduce a new reader: foobar: The reader driver did not produce a unique reader name.  (0x8010001B)"
        else:
            expected = "Failed to introduce a new reader: foobar: Reader already exists. (0x8010001B)"
        self.assertEqual(text, expected)

    def test_RemoveReaderFromGroupException(self):
        exc = RemoveReaderFromGroupException(SCARD_E_INVALID_HANDLE,
            "readername", "readergroup")
        self.assertEqual(exc.hresult, SCARD_E_INVALID_HANDLE)
        text = str(exc)
        if get_platform().startswith('win'):
            expected = "Failed to remove reader: readername from group: readergroup: The supplied handle was invalid.  (0x80100003)"
        else:
            expected = "Failed to remove reader: readername from group: readergroup: Invalid handle. (0x80100003)"
        self.assertEqual(text, expected)

    def test_AddReaderToGroupException(self):
        exc = AddReaderToGroupException(SCARD_E_INVALID_HANDLE,
                "reader", "group")
        self.assertEqual(exc.hresult, SCARD_E_INVALID_HANDLE)
        text = str(exc)
        if get_platform().startswith('win'):
            expected = "Failed to add reader: reader to group: group: The supplied handle was invalid.  (0x80100003)"
        else:
            expected = "Failed to add reader: reader to group: group: Invalid handle. (0x80100003)"
        self.assertEqual(text, expected)

    def test_ReleaseContextException(self):
        exc = ReleaseContextException(SCARD_E_INVALID_HANDLE)
        self.assertEqual(exc.hresult, SCARD_E_INVALID_HANDLE)
        text = str(exc)
        if get_platform().startswith('win'):
            expected = "Failed to release context: The supplied handle was invalid.  (0x80100003)"
        else:
            expected = "Failed to release context: Invalid handle. (0x80100003)"
        self.assertEqual(text, expected)

if __name__ == '__main__':
    unittest.main()
