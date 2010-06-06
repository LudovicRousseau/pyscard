# -*- coding: iso-8859-1 -*-
"""smartcard.util package

__author__ = "http://www.gemalto.com"

Copyright 2001-2010 gemalto
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

PACK = 1
HEX = 2
UPPERCASE = 4
COMMA = 8


def padd(bytelist, length, padding='FF'):
    """ Padds a byte list with a constant byte value (default is x0FF)
        bytelist: the byte list to padd
        length:   the total length of the resulting byte list;
                  no padding if length is smaller than the byte list length
        padding:  padding value (default is 0xff)

        returns the padded bytelist
        example:
        padd(toBytes(\"3B 65 00 00 9C 11 01 01 03\"), 16) returns [0x3B, 0x65, 0, 0, 0x9C, 0x11, 1, 1, 3, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        padd(toBytes(\"3B 65 00 00 9C 11 01 01 03\"), 8) returns [0x3B, 0x65, 0, 0, 0x9C, 0x11, 1, 1, 3 ]

    """

    if len(bytelist) < length:
        for index in range(length - len(bytelist)):
            bytelist.append(eval('0x' + padding))

    return bytelist


def toASCIIBytes(stringtoconvert):
    """Returns a list of ASCII bytes from a string.

       stringtoconvert: the string to convert into a byte list

       returns a byte list of the ASCII codes of the string characters

       toASCIIBytes() is the reverse of toASCIIString()

       example:
       toASCIIBytes("Number 101") returns[ 0x4E, 0x75, 0x6D, 0x62, 0x65, 0x72, 0x20, 0x31, 0x30, 0x31 ]
    """

    return map(ord, list(stringtoconvert))


def toASCIIString(bytelist):
    """Returns a string representing a list of ASCII bytes.

       bytelist: list of ASCII bytes to convert into a string

       returns a string from the ASCII code list

       toASCIIString() is the reverse of toASCIIBytes()

       example:

       toASCIIString([ 0x4E, 0x75, 0x6D, 0x62, 0x65, 0x72, 0x20, 0x31, 0x30, 0x31 ]) returns "Number 101")
    """

    return ''.join(map(chr, bytelist))


def toBytes(bytestring):
    """Returns a list of bytes from a byte string

       bytestring: a byte string of the format \"3B 65 00 00 9C 11 01 01 03\" or \"3B6500009C11010103\" or \"3B6500   009C1101  0103\"
    """
    from struct import unpack
    import re
    packedstring = ''.join(re.split('\W+', bytestring))
    try:
        return reduce(lambda x, y: x + [int(y, 16)], unpack('2s' * (len(packedstring) / 2), packedstring), [])
    except:
        raise TypeError, 'not a string representing a list of bytes'


"""GSM3.38 character conversion table."""
__dic_GSM_3_38__ = {
    '@': 0x00,             # @ At symbol
    '£': 0x01,             # £ Britain pound symbol
    '$': 0x02,             # $ Dollar symbol
    chr(0xA5): 0x03,       # ¥ Yen symbol
    'è': 0x04,             # è e accent grave
    'é': 0x05,             # é e accent aigu
    'ù': 0x06,             # ù u accent grave
    chr(0xEC): 0x07,       # ì i accent grave
    chr(0xF2): 0x08,       # ò o accent grave
    chr(0xC7): 0x09,       # Ç C majuscule cedille
    chr(0x0A): 0x0A,       # LF Line Feed
    chr(0xD8): 0x0B,       # Ø O majuscule barré
    chr(0xF8): 0x0C,       # ø o minuscule barré
    chr(0x0D): 0x0D,       # CR Carriage Return
    chr(0xC5): 0x0E,       # Å Angstroem majuscule
    chr(0xE5): 0x0F,       # å Angstroem minuscule
    '_': 0x11,             # underscore
    chr(0xC6): 0x1C,       # Æ majuscule ae
    chr(0xE6): 0x1D,       # æ minuscule ae
    chr(0xDF): 0x1E,       # ß s dur allemand
    chr(0xC9): 0x1F,       # É majuscule é
    ' ': 0x20,
    '!': 0x21,
    '\"': 0x22,            # guillemet
    '#': 0x23,
    '¤': 0x24,             # ¤ carré
    chr(0xA1): 0x40,       # ¡ point d'exclamation renversé
    chr(0xC4): 0x5B,       # Ä majuscule A trema
    chr(0xE4): 0x7B,       # ä minuscule a trema
    chr(0xD6): 0x5C,       # Ö majuscule O trema
    chr(0xF6): 0x7C,       # ö minuscule o trema
    chr(0xD1): 0x5D,       # Ñ majuscule N tilda espagnol
    chr(0xF1): 0x7D,       # ñ minuscule n tilda espagnol
    chr(0xDC): 0x5E,       # Ü majuscule U trema
    chr(0xFC): 0x7E,       # ü minuscule u trema
    chr(0xA7): 0x5F,       # § signe paragraphe
    chr(0xBF): 0x60,       # ¿ point interrogation renversé
    'à': 0x7F              # a accent grave
}


def toGSM3_38Bytes(stringtoconvert):
    """Returns a list of bytes from a string using GSM 3.38 conversion table.

       stringtoconvert:     string to convert

       returns a list of bytes

       example:
       toGSM3_38Bytes("@ùPascal") returns [ 0x00, 0x06, 0x50, 0x61, 0x73, 0x63, 0x61, 0x6C ]
    """

    bytes = []
    for char in stringtoconvert:
        if ((char >= "%") and (char <= "?")):
            bytes.append(ord(char))
        elif ((char >= "A") and (char <= "Z")):
            bytes.append(ord(char))
        elif ((char >= "a") and (char <= "z")):
            bytes.append(ord(char))
        else:
            bytes.append(int(__dic_GSM_3_38__[char]))
    return bytes


def toHexString(bytes=[], format=0):
    """Returns an hex string representing bytes

        bytes:  a list of bytes to stringify, e.g. [59, 22, 148, 32, 2, 1, 0, 0, 13]
        format: a logical OR of
                COMMA: add a comma between bytes
                HEX: add the 0x chars before bytes
                UPPERCASE: use 0X before bytes (need HEX)
                PACK: remove blanks

        example:
        bytes = [ 0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03 ]

        toHexString(bytes) returns  3B 65 00 00 9C 11 01 01 03

        toHexString(bytes, COMMA) returns  3B, 65, 00, 00, 9C, 11, 01, 01, 03
        toHexString(bytes, HEX) returns  0x3B 0x65 0x00 0x00 0x9C 0x11 0x01 0x01 0x03
        toHexString(bytes, HEX | COMMA) returns  0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03

        toHexString(bytes, PACK) returns  3B6500009C11010103

        toHexString(bytes, HEX | UPPERCASE) returns  0X3B 0X65 0X00 0X00 0X9C 0X11 0X01 0X01 0X03
        toHexString(bytes, HEX | UPPERCASE | COMMA) returns  0X3B, 0X65, 0X00, 0X00, 0X9C, 0X11, 0X01, 0X01, 0X03
    """

    from string import rstrip

    for byte in tuple(bytes):
        pass

    if type(bytes) is not list:
        raise TypeError, 'not a list of bytes'

    if bytes == None or bytes == []:
        return ""
    else:
        pformat = "%-0.2X"
        if COMMA & format:
            pformat = pformat + ","
        pformat = pformat + " "
        if PACK & format:
            pformat = rstrip(pformat)
        if HEX & format:
            if UPPERCASE & format:
                pformat = "0X" + pformat
            else:
                pformat = "0x" + pformat
        return rstrip(rstrip(reduce(lambda a, b: a + pformat % ((b + 256) % 256), [""] + bytes)), ',')


def HexListToBinString(hexlist):
    binstring = ""
    for byte in hexlist:
        binstring = binstring + chr(eval('0x%x' % byte))
    return binstring


def BinStringToHexList(binstring):
    hexlist = []
    for byte in binstring:
        hexlist = hexlist + [ord(byte)]
    return hexlist


def hl2bs(hexlist):
    return HexListToBinString(hexlist)


def bs2hl(binstring):
    return BinStringToHexList(binstring)
