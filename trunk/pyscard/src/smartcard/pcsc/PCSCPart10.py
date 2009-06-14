"""PCSCPart10: PC/SC Part 10 (pinpad)

__author__ = "Ludovic Rousseau"

Copyright 2009 Ludovic Rosseau
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

# constants defined in PC/SC v2 Part 10
CM_IOCTL_GET_FEATURE_REQUEST  = SCARD_CTL_CODE(3400)

FEATURE_VERIFY_PIN_START         = 0x01
FEATURE_VERIFY_PIN_FINISH        = 0x02
FEATURE_MODIFY_PIN_START         = 0x03
FEATURE_MODIFY_PIN_FINISH        = 0x04
FEATURE_GET_KEY_PRESSED          = 0x05
FEATURE_VERIFY_PIN_DIRECT        = 0x06
FEATURE_MODIFY_PIN_DIRECT        = 0x07
FEATURE_MCT_READERDIRECT         = 0x08
FEATURE_MCT_UNIVERSAL            = 0x09
FEATURE_IFD_PIN_PROPERTIES       = 0x0A
FEATURE_ABORT                    = 0x0B
FEATURE_SET_SPE_MESSAGE          = 0x0C
FEATURE_VERIFY_PIN_DIRECT_APP_ID = 0x0D
FEATURE_MODIFY_PIN_DIRECT_APP_ID = 0x0E
FEATURE_WRITE_DISPLAY            = 0x0F
FEATURE_GET_KEY                  = 0x10
FEATURE_IFD_DISPLAY_PROPERTIES   = 0x11

Features = {
"FEATURE_VERIFY_PIN_START"         : FEATURE_VERIFY_PIN_START,
"FEATURE_VERIFY_PIN_FINISH"        : FEATURE_VERIFY_PIN_FINISH,
"FEATURE_MODIFY_PIN_START"         : FEATURE_MODIFY_PIN_START,
"FEATURE_MODIFY_PIN_FINISH"        : FEATURE_MODIFY_PIN_FINISH,
"FEATURE_GET_KEY_PRESSED"          : FEATURE_GET_KEY_PRESSED,
"FEATURE_VERIFY_PIN_DIRECT"        : FEATURE_VERIFY_PIN_DIRECT,
"FEATURE_MODIFY_PIN_DIRECT"        : FEATURE_MODIFY_PIN_DIRECT,
"FEATURE_MCT_READERDIRECT"         : FEATURE_MCT_READERDIRECT,
"FEATURE_MCT_UNIVERSAL"            : FEATURE_MCT_UNIVERSAL,
"FEATURE_IFD_PIN_PROPERTIES"       : FEATURE_IFD_PIN_PROPERTIES,
"FEATURE_ABORT"                    : FEATURE_ABORT,
"FEATURE_SET_SPE_MESSAGE"          : FEATURE_SET_SPE_MESSAGE,
"FEATURE_VERIFY_PIN_DIRECT_APP_ID" : FEATURE_VERIFY_PIN_DIRECT_APP_ID,
"FEATURE_MODIFY_PIN_DIRECT_APP_ID" : FEATURE_MODIFY_PIN_DIRECT_APP_ID,
"FEATURE_WRITE_DISPLAY"            : FEATURE_WRITE_DISPLAY,
"FEATURE_GET_KEY"                  : FEATURE_GET_KEY,
"FEATURE_IFD_DISPLAY_PROPERTIES"   : FEATURE_IFD_DISPLAY_PROPERTIES
}

# we already have:       Features['FEATURE_x'] = FEATURE_x
# we will now also have: Features[FEATURE_x] = 'FEATURE_x'
for k in Features.keys():
    Features[Features[k]] = k

def getFeatureRequest(cardConnection):
    """ Get the list of Part10 features supported by the reader.

    cardConnection: CardConnection object

    return: a list of list [[tag1, value1], [tag2, value2]]
    """
    response = cardConnection.control(CM_IOCTL_GET_FEATURE_REQUEST, [])
    features = []
    while (len(response) > 0):
        tag = response[0]
        control = (((((response[2]<<8) + response[3])<<8) + response[4])<<8) + response[5]
        features.append([Features[tag], control])
        del response[:6]
    return features

def hasFeature(featureList, feature):
    """ return the controlCode for a feature or None

    feature:     feature to look for
    featureList: feature list as returned by getFeatureRequest()

    return: feature value or None
    """
    for f in featureList:
        if f[0] == feature or Features[f[0]] == feature:
            return f[1]

def getPinProperties(cardConnection, featureList = None, controlCode = None):
    """ return the PIN_PROPERTIES structure

    cardConnection: CardConnection object
    featureList: feature list as returned by getFeatureRequest()
    controlCode: control code for FEATURE_IFD_PIN_PROPERTIES

    return: a dict """
    if controlCode is None:
        if featureList is None:
            featureList = getFeatureRequest(cardConnection)
        controlCode = hasFeature(featureList, FEATURE_IFD_PIN_PROPERTIES)

    if controlCode is None:
        return

    response = cardConnection.control(controlCode, [])
    d = {
            'raw': response,
            'LcdLayoutX': response[0],
            'LcdLayoutY': response[1],
            'LcdMaxCharacters': response[2]<<8 + response[3],
            'LcdMaxLines': response[4]<<8 + response[5],
            'EntryValidationCondition': response[6],
            'TimeOut2': response[7]
        }

    return d

if __name__ == '__main__':
    """Small sample illustrating the use of PCSCPart10."""
    from smartcard.pcsc.PCSCReader import readers
    cc = readers()[0].createConnection()
    cc.connect()

    #print cc.control( CM_IOCTL_GET_FEATURE_REQUEST )
    features = getFeatureRequest(cc)
    print features

    print hasFeature(features, FEATURE_VERIFY_PIN_START)
    print hasFeature(features, FEATURE_VERIFY_PIN_DIRECT)

    print getPinProperties(cc)
