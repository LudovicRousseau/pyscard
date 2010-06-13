#! /usr/bin/env python
"""
Sample for python PCSC wrapper module: send a Control Code to a card or
reader

__author__ = "Ludovic Rousseau"

Copyright 2009-2010 Ludovic Rousseau
Author: Ludovic Rousseau, mailto:ludovic.rousseau@free.fr

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

from smartcard.scard import *
from smartcard.util import toASCIIBytes


def can_do_verify_pin(hCard):
    FEATURE_VERIFY_PIN_DIRECT = 6
    return parse_get_feature_request(hCard, FEATURE_VERIFY_PIN_DIRECT)


def can_do_modify_pin(hCard):
    FEATURE_MODIFY_PIN_DIRECT = 7
    return parse_get_feature_request(hCard, FEATURE_MODIFY_PIN_DIRECT)


def parse_get_feature_request(hCard, feature):
    # check the reader can do a verify pin
    CM_IOCTL_GET_FEATURE_REQUEST = SCARD_CTL_CODE(3400)
    hresult, response = SCardControl(hcard, CM_IOCTL_GET_FEATURE_REQUEST, [])
    if hresult != SCARD_S_SUCCESS:
        raise error, 'SCardControl failed: ' + SCardGetErrorMessage(hresult)
    print response
    while (len(response) > 0):
        tag = response[0]
        if (feature == tag):
            return (((((response[2] << 8) + response[3]) << 8) + response[4]) << 8) + response[5]
        response = response[6:]


def verifypin(hCard, control=None):
    if None == control:
        control = can_do_verify_pin(hCard)
        if (None == control):
            raise error, "Not a pinpad"
    hresult, response = SCardControl(hcard, control, [])
    if hresult != SCARD_S_SUCCESS:
        raise error, 'SCardControl failed: ' + SCardGetErrorMessage(hresult)
    return hresult, response

try:
    hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
    if hresult != SCARD_S_SUCCESS:
        raise error, 'Failed to establish context: ' + SCardGetErrorMessage(hresult)
    print 'Context established!'

    try:
        hresult, readers = SCardListReaders(hcontext, [])
        if hresult != SCARD_S_SUCCESS:
            raise error, 'Failed to list readers: ' + SCardGetErrorMessage(hresult)
        print 'PCSC Readers:', readers

        if len(readers) < 1:
            raise error, 'No smart card readers'

        for zreader in readers:

            print 'Trying to Control reader:', zreader

            try:
                hresult, hcard, dwActiveProtocol = SCardConnect(
                    hcontext, zreader, SCARD_SHARE_DIRECT, SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
                if hresult != SCARD_S_SUCCESS:
                    raise error, 'Unable to connect: ' + SCardGetErrorMessage(hresult)
                print 'Connected with active protocol', dwActiveProtocol

                try:
                    cmd_verify = can_do_verify_pin(hcard)
                    if (cmd_verify):
                        print "can do verify pin: 0x%08X" % cmd_verify

                    cmd_modify = can_do_modify_pin(hcard)
                    if (cmd_modify):
                        print "can do modify pin: 0x%08X" % cmd_modify

                    (hresult, response) = verifypin(hcard, cmd_verify)
                    r = ""
                    for i in xrange(len(response)):
                        r += "%c" % response[i]
                    print 'Control:', r
                finally:
                    hresult = SCardDisconnect(hcard, SCARD_UNPOWER_CARD)
                    if hresult != SCARD_S_SUCCESS:
                        raise error, 'Failed to disconnect: ' + SCardGetErrorMessage(hresult)
                    print 'Disconnected'

            except error, (message):
                print error, message

    finally:
        hresult = SCardReleaseContext(hcontext)
        if hresult != SCARD_S_SUCCESS:
            raise error, 'Failed to release context: ' + SCardGetErrorMessage(hresult)
        print 'Released context.'

except error, e:
    print e

import sys
if 'win32' == sys.platform:
    print 'press Enter to continue'
    sys.stdin.read(1)
