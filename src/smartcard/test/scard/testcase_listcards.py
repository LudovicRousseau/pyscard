#! /usr/bin/env python3
"""Unit tests for SCardIntroduceCardType/SCardListCards/SCardListInterfaces

This test case can be executed individually, or with all other test cases
thru testsuite_scard.py.

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


import platform
import unittest

import smartcard.guid
from smartcard.scard import *

if "winscard" == resourceManager:

    class testcase_listcards(unittest.TestCase):
        """Test scard API for ATR retrieval"""

        # setup for all unit tests: establish context and introduce
        # a dummy card interface
        def setUp(self):
            hresult, self.hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
            self.assertEqual(hresult, 0)
            self.dummycardname = "dummycard"
            self.dummycardATR = [
                0x3B,
                0x75,
                0x94,
                0x00,
                0x00,
                0x62,
                0x02,
                0x02,
                0x01,
                0x01,
            ]
            self.dummycardMask = [
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0x00,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
            ]
            self.dummycardguid1 = smartcard.guid.strToGUID(
                "{AD4F1667-EA75-4124-84D4-641B3B197C65}"
            )
            self.dummycardguid2 = smartcard.guid.strToGUID(
                "{382AE95A-7C2C-449c-A179-56C6DE6FF3BC}"
            )
            testcase_listcards.__introduceinterface(self)

        # teardown for all unit tests: release context and forget
        # dummy card interface
        def tearDown(self):
            testcase_listcards.__forgetinterface(self)
            hresult = SCardReleaseContext(self.hcontext)
            self.assertEqual(hresult, 0)

        # introduce a dummy card interface
        # card ATR same as e-gate
        def __introduceinterface(self):
            hresult = SCardForgetCardType(self.hcontext, self.dummycardname)
            dummycardPrimaryGUID = self.dummycardguid1
            dummycardGUIDS = self.dummycardguid1 + self.dummycardguid2
            hresult = SCardIntroduceCardType(
                self.hcontext,
                self.dummycardname,
                dummycardPrimaryGUID,
                dummycardGUIDS,
                self.dummycardATR,
                self.dummycardMask,
            )
            self.assertEqual(hresult, 0)

        # forget dummy card interface
        def __forgetinterface(self):
            hresult = SCardForgetCardType(self.hcontext, self.dummycardname)
            self.assertEqual(hresult, 0)

        # locate a known card
        # Cryptoflex 8k v2 is present in standard Windows 2000
        def test_listcryptoflexbyatr(self):
            slbCryptoFlex8kv2ATR = [
                0x3B,
                0x95,
                0x15,
                0x40,
                0x00,
                0x68,
                0x01,
                0x02,
                0x00,
                0x00,
            ]
            slbCryptoFlex8kv2Name = ["Schlumberger Cryptoflex 8K v2"]
            hresult, card = SCardListCards(self.hcontext, slbCryptoFlex8kv2ATR, [])
            self.assertEqual(hresult, 0)
            self.assertEqual(card, slbCryptoFlex8kv2Name)

        # locate dummy card by interface
        def test_listdummycardbyguid(self):
            guidstolocate = self.dummycardguid2 + self.dummycardguid1
            locatedcardnames = [self.dummycardname]
            hresult, card = SCardListCards(self.hcontext, [], guidstolocate)
            self.assertEqual(hresult, 0)
            self.assertEqual(card, locatedcardnames)

        # list our dummy card interfaces and check
        # that they match the introduced interfaces
        def test_listdummycardinterfaces(self):
            hresult, interfaces = SCardListInterfaces(self.hcontext, self.dummycardname)
            self.assertEqual(hresult, 0)
            self.assertEqual(2, len(interfaces))
            self.assertEqual(self.dummycardguid1, interfaces[0])
            self.assertEqual(self.dummycardguid2, interfaces[1])

        # locate all cards and interfaces in the system
        def test_listallcards(self):

            # dummycard has been introduced in the test setup and
            # will be removed in the test teardown. Other cards are
            # the cards present by default on Windows 2000
            expectedCards = [
                "dummycard",
                "GemSAFE Smart Card (8K)",
                "Schlumberger Cryptoflex 4K",
                "Schlumberger Cryptoflex 8K",
                "Schlumberger Cryptoflex 8K v2",
            ]
            hresult, cards = SCardListCards(self.hcontext, [], [])
            self.assertEqual(hresult, 0)
            foundCards = {}
            for i in range(len(cards)):
                foundCards[cards[i]] = 1
            for i in expectedCards:
                self.assertTrue(i in foundCards)

            # dummycard has a primary provider,
            # other cards have no primary provider
            expectedPrimaryProviderResult = {
                "dummycard": [0, self.dummycardguid1],
                "GemSAFE": [2, None],
                "Schlumberger Cryptoflex 4k": [2, None],
                "Schlumberger Cryptoflex 8k": [2, None],
                "Schlumberger Cryptoflex 8k v2": [2, None],
            }
            for i in range(len(cards)):
                hresult, providername = SCardGetCardTypeProviderName(
                    self.hcontext, cards[i], SCARD_PROVIDER_PRIMARY
                )
                if cards[i] in expectedPrimaryProviderResult:
                    self.assertEqual(
                        hresult, expectedPrimaryProviderResult[cards[i]][0]
                    )
                    if hresult == SCARD_S_SUCCESS:
                        self.assertEqual(
                            providername,
                            smartcard.guid.GUIDToStr(
                                expectedPrimaryProviderResult[cards[i]][1]
                            ),
                        )

            # dummycard has no CSP, other cards have a CSP
            expectedProviderCSPResult = {
                "dummycard": [2, None],
                "GemSAFE": [0, "Gemplus GemSAFE Card CSP v1.0"],
                "Schlumberger Cryptoflex 4k": [
                    0,
                    "Schlumberger Cryptographic Service Provider",
                ],
                "Schlumberger Cryptoflex 8k": [
                    0,
                    "Schlumberger Cryptographic Service Provider",
                ],
                "Schlumberger Cryptoflex 8k v2": [
                    0,
                    "Schlumberger Cryptographic Service Provider",
                ],
            }
            for i in range(len(cards)):
                hresult, providername = SCardGetCardTypeProviderName(
                    self.hcontext, cards[i], SCARD_PROVIDER_CSP
                )
                if cards[i] in expectedProviderCSPResult:
                    self.assertEqual(hresult, expectedProviderCSPResult[cards[i]][0])
                    self.assertEqual(
                        providername, expectedProviderCSPResult[cards[i]][1]
                    )

    def suite():
        suite1 = unittest.defaultTestLoader.loadTestsFromTestCase(testcase_listcards)
        return unittest.TestSuite(suite1)


if __name__ == "__main__":
    unittest.main()
