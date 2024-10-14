#! /usr/bin/env python3
"""Generates test suite smartcard configuration from
connected readers and cards.

The generated configuration is store in local_config.py.

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


import os.path
import time

from smartcard.ATR import ATR
from smartcard.Exceptions import NoCardException
from smartcard.System import readers


def getATR(reader):
    """
    Get card ATR
    """
    cc = reader.createConnection()
    cc.connect()
    atr = cc.getATR()
    cc.disconnect()
    return atr


def checklocalconfig():
    """
    Generate or regenerate local_config.py
    """
    if os.path.isfile("local_config.py"):
        print("regenerating local_config.py...")
    else:
        print("local_config.py not found; generating local_config.py...")

    wrong_setup = False
    # generate local configuration
    with open("local_config.py", "w", encoding="utf-8") as f:

        f.write("from smartcard.util import toHexString\n")
        f.write("expectedReaders = ")
        expectedReaders = readers()
        if len(expectedReaders) < 2:
            print("You should use at least 2 readers.")
            wrong_setup = True
        f.write(str(expectedReaders) + "\n")
        expectedATRs = []
        atr_ok = 0
        for reader in expectedReaders:
            try:
                atr = getATR(reader)
                expectedATRs.append(atr)
                if ATR(atr).isT1Supported():
                    print("You should use T=0 cards")
                    wrong_setup = True
                atr_ok += 1
            except NoCardException:
                expectedATRs.append([])
        if atr_ok < 2:
            print("You should use at least 2 cards.")
            wrong_setup = True

        f.write("expectedATRs = ")
        f.write(repr(expectedATRs) + "\n")

        f.write("expectedATRinReader = {}\n")
        f.write("for i in range(len(expectedReaders)):\n")
        f.write("    expectedATRinReader[expectedReaders[i]] = expectedATRs[i]\n")

        f.write("expectedReaderForATR = {}\n")
        f.write("for i in range(len(expectedReaders)):\n")
        f.write(
            "    expectedReaderForATR[toHexString(expectedATRs[i])] = "
            + "expectedReaders[i]\n"
        )

        f.write("expectedReaderGroups = ['SCard$DefaultReaders']\n")

    if wrong_setup:
        print("The readers or cards setup is invalid. Some tests WILL fail!")
        print("Pause for 5 seconds")
        time.sleep(5)


if __name__ == "__main__":
    import sys

    checklocalconfig()
    sys.exit()
