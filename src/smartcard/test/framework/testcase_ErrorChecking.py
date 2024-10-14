#! /usr/bin/env python3
"""Unit tests for smartcard.sw

This test case can be executed individually, or with all other test cases
thru testsuite_framework.py.

__author__ = "https://www.gemalto.com/"

Copyright 2001-2012 gemalto
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


import unittest

import smartcard.sw.SWExceptions
from smartcard.sw.ErrorChecker import ErrorChecker
from smartcard.sw.ErrorCheckingChain import ErrorCheckingChain
from smartcard.sw.ISO7816_4_SW1ErrorChecker import ISO7816_4_SW1ErrorChecker
from smartcard.sw.ISO7816_4ErrorChecker import ISO7816_4ErrorChecker
from smartcard.sw.ISO7816_8ErrorChecker import ISO7816_8ErrorChecker
from smartcard.sw.ISO7816_9ErrorChecker import ISO7816_9ErrorChecker
from smartcard.sw.op21_ErrorChecker import op21_ErrorChecker


class CustomSWException(smartcard.sw.SWExceptions.SWException):
    """Test exception raised by TestErrorChecker."""

    def __init__(self, data, sw1, sw2, message=""):
        smartcard.sw.SWExceptions.SWException.__init__(self, data, sw1, sw2)


class TestErrorChecker(ErrorChecker):
    """Test error checking checker.

    This checker raises the following exception:

    sw1: 56 sw2: 55      CustomSWException
    sw1: 63 sw2: any     WarningProcessingException
    """

    def __call__(self, data, sw1, sw2):
        if 0x56 == sw1 and 0x55 == sw2:
            raise CustomSWException(data, sw1, sw2)
        if 0x63 == sw1:
            raise CustomSWException(data, sw1, sw2)


class testcase_ErrorChecking(unittest.TestCase):
    """Test case for smartcard.sw.* error checking."""

    def failUnlessRaises(self, excClass, callableObj, *args, **kwargs):
        """override of unittest.TestCase.failUnlessRaises so that we return the
        exception object for testing fields."""
        try:
            callableObj(*args, **kwargs)
        except excClass as e:
            return e

        if hasattr(excClass, "__name__"):
            exc_name = excClass.__name__
        else:
            exc_name = str(excClass)
        raise self.failureException(exc_name)

    def testcase_ISO7816_4SW1ErrorChecker(self):
        """Test ISO7816_4_SW1ErrorChecker."""
        ecs = ISO7816_4_SW1ErrorChecker()

        tiso7816_4SW1 = {
            0x62: smartcard.sw.SWExceptions.WarningProcessingException,
            0x63: smartcard.sw.SWExceptions.WarningProcessingException,
            0x64: smartcard.sw.SWExceptions.ExecutionErrorException,
            0x65: smartcard.sw.SWExceptions.ExecutionErrorException,
            0x66: smartcard.sw.SWExceptions.SecurityRelatedException,
            0x67: smartcard.sw.SWExceptions.CheckingErrorException,
            0x68: smartcard.sw.SWExceptions.CheckingErrorException,
            0x69: smartcard.sw.SWExceptions.CheckingErrorException,
            0x6A: smartcard.sw.SWExceptions.CheckingErrorException,
            0x6B: smartcard.sw.SWExceptions.CheckingErrorException,
            0x6C: smartcard.sw.SWExceptions.CheckingErrorException,
            0x6D: smartcard.sw.SWExceptions.CheckingErrorException,
            0x6E: smartcard.sw.SWExceptions.CheckingErrorException,
            0x6F: smartcard.sw.SWExceptions.CheckingErrorException,
        }

        for sw1 in range(0x00, 0xFF + 1):
            exception = tiso7816_4SW1.get(sw1)
            for sw2 in range(0x00, 0xFF + 1):
                if exception is not None:
                    with self.assertRaises(exception):
                        ecs([], sw1, sw2)
                else:
                    ecs([], sw1, sw2)

    def testcase_ISO7816_4ErrorChecker(self):
        """Test ISO7816_4ErrorChecker."""
        ecs = ISO7816_4ErrorChecker()

        tiso7816_4SW = {
            0x62: (
                smartcard.sw.SWExceptions.WarningProcessingException,
                [0x00, 0x81, 0x82, 0x83, 0x84, 0xFF],
            ),
            0x63: (
                smartcard.sw.SWExceptions.WarningProcessingException,
                [0x00, 0x81] + list(range(0xC0, 0xCF + 1)),
            ),
            0x64: (smartcard.sw.SWExceptions.ExecutionErrorException, [0x00]),
            0x67: (smartcard.sw.SWExceptions.CheckingErrorException, [0x00]),
            0x68: (smartcard.sw.SWExceptions.CheckingErrorException, [0x81, 0x82]),
            0x69: (
                smartcard.sw.SWExceptions.CheckingErrorException,
                list(range(0x81, 0x88 + 1)),
            ),
            0x6A: (
                smartcard.sw.SWExceptions.CheckingErrorException,
                list(range(0x80, 0x88 + 1)),
            ),
            0x6B: (smartcard.sw.SWExceptions.CheckingErrorException, [0x00]),
            0x6D: (smartcard.sw.SWExceptions.CheckingErrorException, [0x00]),
            0x6E: (smartcard.sw.SWExceptions.CheckingErrorException, [0x00]),
            0x6F: (smartcard.sw.SWExceptions.CheckingErrorException, [0x00]),
        }

        exception = None
        for sw1 in range(0x00, 0xFF + 1):
            sw2range = []
            if sw1 in tiso7816_4SW:
                exception, sw2range = tiso7816_4SW[sw1]
            for sw2 in range(0x00, 0xFF + 1):
                if sw2 in sw2range:
                    with self.assertRaises(exception):
                        ecs([], sw1, sw2)
                else:
                    ecs([], sw1, sw2)

    def testcase_ISO7816_8ErrorChecker(self):
        """Test ISO7816_4ErrorChecker."""
        ecs = ISO7816_8ErrorChecker()

        tiso7816_8SW = {
            0x63: (
                smartcard.sw.SWExceptions.WarningProcessingException,
                [0x00] + list(range(0xC0, 0xCF + 1)),
            ),
            0x65: (smartcard.sw.SWExceptions.ExecutionErrorException, [0x81]),
            0x66: (
                smartcard.sw.SWExceptions.SecurityRelatedException,
                [0x00, 0x87, 0x88],
            ),
            0x67: (smartcard.sw.SWExceptions.CheckingErrorException, [0x00]),
            0x68: (smartcard.sw.SWExceptions.CheckingErrorException, [0x83, 0x84]),
            0x69: (
                smartcard.sw.SWExceptions.CheckingErrorException,
                list(range(0x82, 0x85 + 1)),
            ),
            0x6A: (
                smartcard.sw.SWExceptions.CheckingErrorException,
                [0x81, 0x82, 0x86, 0x88],
            ),
        }

        exception = None
        for sw1 in range(0x00, 0xFF + 1):
            sw2range = []
            if sw1 in tiso7816_8SW:
                exception, sw2range = tiso7816_8SW[sw1]
            for sw2 in range(0x00, 0xFF + 1):
                if sw2 in sw2range:
                    with self.assertRaises(exception):
                        ecs([], sw1, sw2)
                else:
                    ecs([], sw1, sw2)

    def testcase_ISO7816_9ErrorChecker(self):
        """Test ISO7816_4ErrorChecker."""
        ecs = ISO7816_9ErrorChecker()

        tiso7816_9SW = {
            0x62: (smartcard.sw.SWExceptions.WarningProcessingException, [0x82]),
            0x64: (smartcard.sw.SWExceptions.ExecutionErrorException, [0x00]),
            0x69: (smartcard.sw.SWExceptions.CheckingErrorException, [0x82]),
            0x6A: (
                smartcard.sw.SWExceptions.CheckingErrorException,
                [0x80, 0x84, 0x89, 0x8A],
            ),
        }

        exception = None
        for sw1 in range(0x00, 0xFF + 1):
            sw2range = []
            if sw1 in tiso7816_9SW:
                exception, sw2range = tiso7816_9SW[sw1]
            for sw2 in range(0x00, 0xFF + 1):
                if sw2 in sw2range:
                    with self.assertRaises(exception):
                        ecs([], sw1, sw2)
                else:
                    ecs([], sw1, sw2)

    def testcase_op21_ErrorChecker(self):
        """Test op21_ErrorChecker."""
        ecs = op21_ErrorChecker()

        top21_SW = {
            0x62: (smartcard.sw.SWExceptions.WarningProcessingException, [0x83]),
            0x63: (smartcard.sw.SWExceptions.WarningProcessingException, [0x00]),
            0x64: (smartcard.sw.SWExceptions.ExecutionErrorException, [0x00]),
            0x65: (smartcard.sw.SWExceptions.ExecutionErrorException, [0x81]),
            0x67: (smartcard.sw.SWExceptions.CheckingErrorException, [0x00]),
            0x69: (smartcard.sw.SWExceptions.CheckingErrorException, [0x82, 0x85]),
            0x6A: (
                smartcard.sw.SWExceptions.CheckingErrorException,
                [0x80, 0x81, 0x82, 0x84, 0x86, 0x88],
            ),
            0x6D: (smartcard.sw.SWExceptions.CheckingErrorException, [0x00]),
            0x6E: (smartcard.sw.SWExceptions.CheckingErrorException, [0x00]),
            0x94: (smartcard.sw.SWExceptions.CheckingErrorException, [0x84, 0x85]),
        }

        exception = None
        for sw1 in range(0x00, 0xFF + 1):
            sw2range = []
            if sw1 in top21_SW:
                exception, sw2range = top21_SW[sw1]
            for sw2 in range(0x00, 0xFF + 1):
                if sw2 in sw2range:
                    with self.assertRaises(exception):
                        ecs([], sw1, sw2)
                else:
                    ecs([], sw1, sw2)

    def testcase_ISO78164_Test_ErrorCheckingChain(self):
        """Test error chain with ISO7816-4 checker followed by Test checker."""
        errorchain = []
        errorchain = [
            ErrorCheckingChain(errorchain, ISO7816_4ErrorChecker()),
            ErrorCheckingChain(errorchain, TestErrorChecker()),
        ]

        # ISO7816-4 is answering first on the next, i.e
        # WarningProcessingException
        for sw2 in [0x00, 0x81] + list(range(0xC0, 0xCF + 1)):
            with self.assertRaises(
                smartcard.sw.SWExceptions.WarningProcessingException
            ):
                errorchain[0]([], 0x63, sw2)

    def testcase_Test_ISO78164_ErrorCheckingChain(self):
        """Test error chain with Test checker followed by ISO7816-4 checker."""
        errorchain = []
        errorchain = [
            ErrorCheckingChain(errorchain, TestErrorChecker()),
            ErrorCheckingChain(errorchain, ISO7816_4ErrorChecker()),
        ]

        # TestErrorChecker is answering first, i.e. CustomSWException
        for sw2 in [0x00, 0x81] + list(range(0xC0, 0xCF + 1)):
            with self.assertRaises(CustomSWException):
                errorchain[0]([], 0x63, sw2)

    def testcase_ErrorMessage(self):
        """Test correct exception error message."""
        ecs = ISO7816_4ErrorChecker()

        with self.assertRaises(smartcard.sw.SWExceptions.CheckingErrorException) as e:
            ecs([], 0x69, 0x85)
            self.assertEqual(
                str(e),
                "'Status word exception: checking error - "
                + "Conditions of use not satisfied!'",
            )

        with self.assertRaises(smartcard.sw.SWExceptions.CheckingErrorException) as e:
            ecs([], 0x6B, 0x00)
            self.assertEqual(
                str(e),
                "'Status word exception: checking error - "
                + "Incorrect parameters P1-P2!'",
            )

    def testcase_ISO78164_Test_ErrorCheckingChain_filtering(self):
        """Test error chain with ISO7816-4 checker followed by Test checker."""
        errorchain = []
        errorchain = [
            ErrorCheckingChain(errorchain, ISO7816_8ErrorChecker()),
            ErrorCheckingChain(errorchain, ISO7816_4ErrorChecker()),
            ErrorCheckingChain(errorchain, ISO7816_4_SW1ErrorChecker()),
        ]

        # don't care about Warning Exceptions
        errorchain[0].addFilterException(
            smartcard.sw.SWExceptions.WarningProcessingException
        )

        for sw2 in range(0x00, 0xFF):

            # should not raise
            errorchain[0]([], 0x62, sw2)
            errorchain[0]([], 0x63, sw2)
            # should raise
            self.assertRaises(
                smartcard.sw.SWExceptions.ExecutionErrorException,
                errorchain[0],
                [],
                0x64,
                sw2,
            )


if __name__ == "__main__":
    unittest.main(verbosity=1)
