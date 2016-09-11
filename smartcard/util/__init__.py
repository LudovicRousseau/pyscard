# -*- coding: iso-8859-1 -*-
"""smartcard.util package

__author__ = "http://www.gemalto.com"

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

PACK = 1
HEX = 2
UPPERCASE = 4
COMMA = 8


def padd(bytelist, length, padding='FF'):
    """ Padds a byte list with a constant byte value (default is x0FF)
    @param bytelist: the byte list to padd
    @param length: the total length of the resulting byte list;
                  no padding if length is smaller than the byte list length
    @param padding: padding value (default is 0xff)

    @return: the padded bytelist

    >>> padd([59, 101, 0, 0, 156, 17, 1, 1, 3], 16)
    [59, 101, 0, 0, 156, 17, 1, 1, 3, 255, 255, 255, 255, 255, 255, 255]
    >>> padd([59, 101, 0, 0, 156, 17, 1, 1, 3], 12, '80')
    [59, 101, 0, 0, 156, 17, 1, 1, 3, 128, 128, 128]
    >>> padd([59, 101, 0, 0, 156, 17, 1, 1, 3], 8)
    [59, 101, 0, 0, 156, 17, 1, 1, 3]
    """

    if len(bytelist) < length:
        for index in range(length - len(bytelist)):
            bytelist.append(eval('0x' + padding))

    return bytelist


def toASCIIBytes(stringtoconvert):
    """Returns a list of ASCII bytes from a string.

    @param stringtoconvert: the string to convert into a byte list

    @return: a byte list of the ASCII codes of the string characters

    L{toASCIIBytes()} is the reverse of L{toASCIIString()}

    >>> toASCIIBytes("Number 101")
    [78, 117, 109, 98, 101, 114, 32, 49, 48, 49]
    """

    return list(map(ord, list(stringtoconvert)))


def toASCIIString(bytelist):
    """Returns a string representing a list of ASCII bytes.

    @param bytelist: list of ASCII bytes to convert into a string

    @return: a string from the ASCII code list

    L{toASCIIString()} is the reverse of L{toASCIIBytes()}

    >>> toASCIIString([0x4E,0x75,0x6D,0x62,0x65,0x72,0x20,0x31,0x30,0x31])
    'Number 101'
    """

    return ''.join(map(chr, bytelist))


def toBytes(bytestring):
    """Returns a list of bytes from a byte string

    bytestring: a byte string

    >>> toBytes("3B 65 00 00 9C 11 01 01 03")
    [59, 101, 0, 0, 156, 17, 1, 1, 3]
    >>> toBytes("3B6500009C11010103")
    [59, 101, 0, 0, 156, 17, 1, 1, 3]
    >>> toBytes("3B6500   009C1101  0103")
    [59, 101, 0, 0, 156, 17, 1, 1, 3]
    """
    packedstring = bytestring.replace(' ', '').replace('	','').replace('\n', '')
    try:
        return list(map(lambda x: int(''.join(x), 16), zip(*[iter(packedstring)] * 2)))
    except (KeyError, ValueError):
        raise TypeError('not a string representing a list of bytes')


"""GSM3.38 character conversion table."""
__dic_GSM_3_38__ = {
    u'@': 0x00,            # @ At symbol
    u'£': 0x01,            # £ Britain pound symbol
    u'$': 0x02,            # $ Dollar symbol
    u'¥': 0x03,            # ¥ Yen symbol
    u'è': 0x04,            # è e accent grave
    u'é': 0x05,            # é e accent aigu
    u'ù': 0x06,            # ù u accent grave
    u'ì': 0x07,            # ì i accent grave
    u'ò': 0x08,            # ò o accent grave
    u'Ç': 0x09,            # Ç C majuscule cedille
    u'\n': 0x0A,           # LF Line Feed
    u'Ø': 0x0B,            # Ø O majuscule barré
    u'ø': 0x0C,            # ø o minuscule barré
    u'\r': 0x0D,           # CR Carriage Return
    u'Å': 0x0E,            # Å Angstroem majuscule
    u'å': 0x0F,            # å Angstroem minuscule
    u'_': 0x11,            # underscore
    u'Æ': 0x1C,            # Æ majuscule ae
    u'æ': 0x1D,            # æ minuscule ae
    u'ß': 0x1E,            # ß s dur allemand
    u'É': 0x1F,            # É majuscule é
    u' ': 0x20,
    u'!': 0x21,
    u'"': 0x22,            # guillemet
    u'#': 0x23,
    u'¤': 0x24,            # ¤ carré
    u'¡': 0x40,            # ¡ point d'exclamation renversé
    u'Ä': 0x5B,            # Ä majuscule A trema
    u'ä': 0x7B,            # ä minuscule a trema
    u'Ö': 0x5C,            # Ö majuscule O trema
    u'ö': 0x7C,            # ö minuscule o trema
    u'Ñ': 0x5D,            # Ñ majuscule N tilda espagnol
    u'ñ': 0x7D,            # ñ minuscule n tilda espagnol
    u'Ü': 0x5E,            # Ü majuscule U trema
    u'ü': 0x7E,            # ü minuscule u trema
    u'§': 0x5F,            # § signe paragraphe
    u'¿': 0x60,            # ¿ point interrogation renversé
    u'à': 0x7F,            # à a accent grave
}


def toGSM3_38Bytes(stringtoconvert):
    """Returns a list of bytes from a string using GSM 3.38 conversion table.

    @param stringtoconvert:     string to convert

    @return: a list of bytes

    >>> toGSM3_38Bytes("@ùPascal")
    [0, 6, 80, 97, 115, 99, 97, 108]
    """
    if isinstance(stringtoconvert, bytes):
        stringtoconvert = stringtoconvert.decode('iso8859-1')

    result = []
    for char in stringtoconvert:
        if ((char >= "%") and (char <= "?")):
            result.append(ord(char))
        elif ((char >= "A") and (char <= "Z")):
            result.append(ord(char))
        elif ((char >= "a") and (char <= "z")):
            result.append(ord(char))
        else:
            result.append(__dic_GSM_3_38__[char])
    return result


def toHexString(bytes=[], format=0):
    """Returns an hex string representing bytes

    @param bytes:  a list of bytes to stringify,
                e.g. [59, 22, 148, 32, 2, 1, 0, 0, 13]
    @param format: a logical OR of
      - COMMA: add a comma between bytes
      - HEX: add the 0x chars before bytes
      - UPPERCASE: use 0X before bytes (need HEX)
      - PACK: remove blanks

    >>> vals = [0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03]
    >>> toHexString(vals)
    '3B 65 00 00 9C 11 01 01 03'
    >>> toHexString(vals, COMMA)
    '3B, 65, 00, 00, 9C, 11, 01, 01, 03'
    >>> toHexString(vals, HEX)
    '0x3B 0x65 0x00 0x00 0x9C 0x11 0x01 0x01 0x03'
    >>> toHexString(vals, HEX | COMMA)
    '0x3B, 0x65, 0x00, 0x00, 0x9C, 0x11, 0x01, 0x01, 0x03'
    >>> toHexString(vals, PACK)
    >>> toHexString(vals, HEX | UPPERCASE)
    '0X3B 0X65 0X00 0X00 0X9C 0X11 0X01 0X01 0X03'
    >>> toHexString(vals, HEX | UPPERCASE | COMMA)
    '0X3B, 0X65, 0X00, 0X00, 0X9C, 0X11, 0X01, 0X01, 0X03'
    """

    for byte in tuple(bytes):
        pass

    if type(bytes) is not list:
        raise TypeError('not a list of bytes')

    if bytes == None or bytes == []:
        return ""
    else:
        pformat = "%-0.2X"
        if COMMA & format:
            separator = ","
        else:
            separator = ""
        if not PACK & format:
            separator = separator + " "
        if HEX & format:
            if UPPERCASE & format:
                pformat = "0X" + pformat
            else:
                pformat = "0x" + pformat
        return (separator.join(map(lambda a: pformat % ((a + 256) % 256), bytes))).rstrip()


# FIXME This appears to duplicate toASCIIString()
def HexListToBinString(hexlist):
    """
    >>> HexListToBinString([78, 117, 109, 98, 101, 114, 32, 49, 48, 49])
    'Number 101'
    """
    return ''.join(map(chr, hexlist))


# FIXME This appears to duplicate to ASCIIBytes()
def BinStringToHexList(binstring):
    """
    >>> BinStringToHexList("Number 101")
    [78, 117, 109, 98, 101, 114, 32, 49, 48, 49]
    """
    return list(map(ord, binstring))


def hl2bs(hexlist):
    """An alias for HexListToBinString

    >>> hl2bs([78, 117, 109, 98, 101, 114, 32, 49, 48, 49])
    'Number 101'
    """
    return HexListToBinString(hexlist)


def bs2hl(binstring):
    """An alias for BinStringToHexList

    >>> bs2hl("Number 101")
    [78, 117, 109, 98, 101, 114, 32, 49, 48, 49]
    """
    return BinStringToHexList(binstring)
