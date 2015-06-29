.. _pyscard_user_guide:

pyscard user's guide
####################

Copyright
*********

| Copyright 2001-2009 `Gemalto <http://www.gemalto.com/>`_
| Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com

This file is part of pyscard.

pyscard is free software; you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the
Free Software Foundation; either version 2.1 of the License, or (at your
option) any later version.

pyscard is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyscard; if not, write to the Free Software Foundation, Inc.,
51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA


Introduction
************

The pyscard smartcard library is a framework for building smart card
aware applications in Python. The smartcard module is built on top of
the PCSC API Python wrapper module.

pyscard supports Windows 2000 and XP by using the `Microsoft Smart Card
Base <http://msdn2.microsoft.com/en-us/library/aa374731.aspx#smart_card_functions>`_ components, and linux and Mac OS X by using `PCSC-lite <http://pcsclite.alioth.debian.org/>`_.


Smart Cards
***********

Smart cards are plastic cards having generally the size of a credit card
and embedding a microprocessor. Smart cards communicate with the outside
world thru a serial port interface and an half-duplex protocol.
Smartcards usually interface with a dedicated terminal, such as a
point-of-sale terminal or a mobile phone. Sometime, smart cards have to
be interfaced with personal computers. This is the case for some
applications such as secure login, mail cyphering or digital signature,
but also for some PC based smart card tools used to personnalize or edit
the content of smart cards. Smart cards are interfaced with a personnal
computer using a smart card reader. The smart card reader connects on
one side to the serial port of the smart card, and on the other side to
the PC, often nowadays thru a USB port.

The PCSC workgroup has defined a standard API to interface smart card
and smart card readers to a PC. The resulting reference implementation
on linux and Mac OS X operating systems is `PC/SC-lite
<http://pcsclite.alioth.debian.org/>`_. All windows operating systems
also include out of the box smart card support, usually called `PCSC
<http://msdn2.microsoft.com/en-us/library/aa374731.aspx#smart_card_functions>`_.

The PCSC API is implemented in C language, and several bridges are
provided to access the PCSC API from different languages such as java or
visual basic. pyscard is a python framework to develop smart card PC
applications on linux, Mac OS X and windows. pyscard lower layers
interface to the PCSC API to access the smart cards and smart card
readers.


Quick-start
***********

We will see in this section some variations on how to send APDU commands
to a smart card.


The reader-centric approach
===========================

A PC application interacts with a card by sending list of bytes, known
as Application Protocol Data Units (APDU). The format of these APDUs is
defined in the ISO7816-4 standard. To send APDUs to a card, the
application needs first to connect to a card thru a smart card reader.
Smart card aware applications that first select a smart card reader,
then connect to the card inserted in the smart card reader use the
reader-centric approach.

In the reader-centric approach, we open a connection with a card thru a
smart card reader, and send APDU commands to the card using the
connection:

.. sourcecode:: python

    >>> from smartcard.System import readers
    >>> from smartcard.util import toHexString
    >>>
    >>> r=readers()
    >>> print r
    ['SchlumbergerSema Reflex USB v.2 0', 'Utimaco CardManUSB 0']
    >>> connection = r[0].createConnection()
    >>> connection.connect()
    >>> SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    >>> DF_TELECOM = [0x7F, 0x10]
    >>> data, sw1, sw2 = connection.transmit( SELECT + DF_TELECOM )
    >>> print "%x %x" % (sw1, sw2)
    9f 1a
    >>>

The list of available readers is retrieved with the readers() function.
We create a connection with the first reader (index 0 for reader 1, 1
for reader 2, ...) with the r[0].createConnection() call and connect to
the card with the connect() method of the connection. We can then send
APDU commands to the card with the transmit() method.

Scripts written with the reader centric approach however have the
following drawbacks:

* the reader index or reader name is hardcoded in the scripts; the
  scripts must be edited to match each user configuration; for example
  in the previous script, we would have to edit the script and change
  r[0] to r[1] for using the second reader

* there is no a-priori knowledge that the card is in the reader; to
  detect card insertion, we would have to execute the script and
  eventually catch a CardConnectionException that would indicate that
  there is no card in the reader.

* there is no built-in check that the card in the reader is of the card
  type we expect; in the previous example, we might try to select the
  DF_TELECOM of an EMV card.

Most of these issues are solved with the card-centric approach, based on
card type detection techniques, such as using the Answer To Reset (ATR)
of the card.


The Answer To Reset (ATR)
=========================

The first answer of a smart card inserted in a smart card reader is call
the ATR. The purpose of the ATR is to describe the supported
communication parameters. The smart card reader, smart card reader
driver, and operating system will use these parameters to establish a
communication with the card. The ATR is described in the ISO7816-3
standard. The first bytes of the ATR describe the voltage convention
(direct or inverse), followed by bytes describing the available
communication interfaces and their respective parameters. These
interface bytes are then followed by Historical Bytes which are not
standardized, and are useful for transmitting proprietary informations
such as the card type, the version of the embedded software, or the card
state. Finally these historical bytes are eventually followd by a
checksum byte.

The class `smartcard.ATR
<http://pyscard.sourceforge.net/epydoc/smartcard.ATR.ATR-class.html>`_
is a pyscard utility class that can interpret the content of an ATR:

.. sourcecode:: python

    #! /usr/bin/env python
    from smartcard.ATR import ATR
    from smartcard.util import toHexString

    atr = ATR([0x3B, 0x9E, 0x95, 0x80, 0x1F, 0xC3, 0x80, 0x31, 0xA0,
        0x73, 0xBE, 0x21, 0x13, 0x67, 0x29, 0x02, 0x01, 0x01, 0x81,0xCD,0xB9] )
    print atr
    print 'historical bytes: ', toHexString( atr.getHistoricalBytes() )
    print 'checksum:', "0x%X" % atr.getChecksum()
    print 'checksum OK:', atr.checksumOK
    print 'T0 supported:', atr.isT0Supported()
    print 'T1 supported:', atr.isT1Supported()
    print 'T15 supported:', atr.isT15Supported()

Which results in the following output::

    3B 9E 95 80 1F C3 80 31 A0 73 BE 21 13 67 29 02 01 01 81 CD B9
    historical bytes: 80 31 A0 73 BE 21 13 67 29 02 01 01 81 CD
    checksum: 0xB9
    checksum OK: True
    T0 supported: True
    T1 supported: False
    T15 supported: True

In practice, the ATR can be used to detect a particular card, either by
trying to match a card with a complete ATR, or by matching a card with
some data in the historical bytes. Smart card aware PC applications that
detects smart cards based on the content of the ATR use the card-centric
approach, independently on the smart card reader in which the card is
inserted..


The card-centric approach
=========================

In the card-centric approach, we create a request for a specific type of
card and wait until a card matching the request is inserted. Once a
matching card is introduced, a connection to the card is automatically
created and we can send APDU commands to the card using this connection.

Requesting a card by ATR
------------------------

The following scripts requests a card with a known ATR::

    >>> from smartcard.CardType import ATRCardType
    >>> from smartcard.CardRequest import CardRequest
    >>> from smartcard.util import toHexString, toBytes
    >>>
    >>> cardtype = ATRCardType( toBytes( "3B 16 94 20 02 01 00 00 0D" ) )
    >>> cardrequest = CardRequest( timeout=1, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()
    >>>
    >>> cardservice.connection.connect()
    >>> print toHexString( cardservice.connection.getATR() )
    3B 16 94 20 02 01 00 00 0D
    >>>
    >>> SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    >>> DF_TELECOM = [0x7F, 0x10]
    >>> data, sw1, sw2 = cardservice.connection.transmit( SELECT + DF_TELECOM )
    >>> print "%x %x" % (sw1, sw2)
    9f 1a
    >>>

To request a card with a know ATR, you must first create an `ATRCardType
<http://pyscard.sourceforge.net/epydoc/smartcard.CardType.ATRCardType-class.html>`_
object with the desired ATR::

    >>> cardtype = ATRCardType( toBytes( "3B 16 94 20 02 01 00 00 0D" ) )

And then create a `CardRequest
<http://pyscard.sourceforge.net/epydoc/smartcard.CardRequest.CardRequest-class.html>`_
for this card type. In the sample, we request a time-out of 1 second.

    >>> cardrequest = CardRequest( timeout=1, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()

The waitforcard() will either return with a card service or a time-out.
The card service connection attribute can be used thereafter to transmit
APDU commands to the card, as with the reader centric approach.

    >>> cardservice.connection.connect()
    >>> print toHexString( cardservice.connection.getATR() )

If necessary, the reader used for the connection can be accessed thru
the `CardConnection
<http://pyscard.sourceforge.net/epydoc/smartcard.CardConnection.CardConnection-class.html>`_
object:

    >>> print cardservice.connection.getReader()
    SchlumbergerSema Reflex USB v.2 0

The `ATRCardType
<http://pyscard.sourceforge.net/epydoc/smartcard.CardType.ATRCardType-class.html>`_
also supports masks:

    >>> from smartcard.CardType import ATRCardType
    >>> from smartcard.CardRequest import CardRequest
    >>> from smartcard.util import toHexString, toBytes
    >>>
    >>> cardtype = ATRCardType( toBytes( "3B 15 94 20 02 01 00 00 0F" ), toBytes( "00 00 FF FF FF FF FF FF 00" ) )
    >>> cardrequest = CardRequest( timeout=1, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()
    >>>
    >>> cardservice.connection.connect()
    >>> print toHexString( cardservice.connection.getATR() )
    3B 16 94 20 02 01 00 00 0D

Other CardTypes are available, and new CardTypes can be created, as
described below.

Requesting any card
-------------------

The `AnyCardType
<http://pyscard.sourceforge.net/epydoc/smartcard.CardType.AnyCardType-class.html>`_
is useful for requesting any card in any reader:

    >>> from smartcard.CardType import AnyCardType
    >>> from smartcard.CardRequest import CardRequest
    >>> from smartcard.util import toHexString
    >>>
    >>> cardtype = AnyCardType()
    >>> cardrequest = CardRequest( timeout=1, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()
    >>>
    >>> cardservice.connection.connect()
    >>> print toHexString( cardservice.connection.getATR() )
    3B 16 94 20 02 01 00 00 0D
    >>> print cardservice.connection.getReader()
    SchlumbergerSema Reflex USB v.2 0

Custom CardTypes
----------------

Custom CardTypes can be created, e.g. a card type that checks the ATR
and the historical bytes of the card. To create a custom CardType,
deriver your CardType class from the `CardType
<http://pyscard.sourceforge.net/epydoc/smartcard.CardType.CardType-class.html>`_
base class (or any other CardType) and override the matches() method.
For exemple to create a DCCardType that will match cards with the direct
convention (first byte of ATR to 0x3b):

    >>> from smartcard.CardType import CardType
    >>> from smartcard.CardRequest import CardRequest
    >>> from smartcard.util import toHexString
    >>>
    >>> class DCCardType(CardType):
    ...      def matches( self, atr, reader=None ):
    ...          return atr[0]==0x3B
    ...
    >>> cardtype = DCCardType()
    >>> cardrequest = CardRequest( timeout=1, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()
    >>>
    >>> cardservice.connection.connect()
    >>> print toHexString( cardservice.connection.getATR() )
    3B 16 94 20 02 01 00 00 0D
    >>> print cardservice.connection.getReader()
    SchlumbergerSema Reflex USB v.2 0
    >>>

Scripts written with the card-centric approach fixes the problems of the
reader-centric approach:

* there is no assumption concerning the reader index or reader name; the
  desired card will be located in any reader

* the request will block or time-out if the desired card type is not
  inserted since we request the desired card type, the script is not
  played on an unknown or uncompatible card

Scripts written with the card-centric approach have however the
following drawbacks:

* the script is limited to a specific card type; we have to modify the
  script if we want to execute the script on another card type. For
  exemple, we have to modify the ATR of the card if we are using the
  ATRCardType. This can be partially solved by having a custom CardType
  that matches several ATRs, though.

Selecting the card communication protocol
-----------------------------------------

Communication parameters are mostly important for the protocol
negociation between the smart card reader and the card. The main
smartcard protocols are the T=0 protocol and the T=1 protocol, for byte
or block transmission, respectively. The required protocol can be
specified at card connection or card transmission.

By defaults, the connect() method of the CardConnection object.will try
to connect using either the T=0 or T=1 protocol. To force a connection
protocol, you can pass the required protocol to the connect() method.

    >>> from smartcard.CardType import AnyCardType
    >>> from smartcard.CardConnection import CardConnection
    >>> from smartcard.CardRequest import CardRequest
    >>> from smartcard.util import toHexString
    >>>
    >>> cardtype = AnyCardType()
    >>> cardrequest = CardRequest( timeout=1, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()
    >>>
    >>> cardservice.connection.connect( CardConnection.T1_protocol )
    >>> print toHexString( cardservice.connection.getATR() )
    3B 16 94 20 02 01 00 00 0D
    >>> print cardservice.connection.getReader()
    SchlumbergerSema Reflex USB v.2 0

Alternatively, you can specify the required protocol in the
CardConnection transmit() method:

    >>> from smartcard.CardType import AnyCardType
    >>> from smartcard.CardConnection import CardConnection
    >>> from smartcard.CardRequest import CardRequest
    >>> from smartcard.util import toHexString, toBytes
    >>>
    >>> cardtype = AnyCardType()
    >>> cardrequest = CardRequest( timeout=1, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()
    >>>
    >>> cardservice.connection.connect()
    >>>
    >>> SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    >>> DF_TELECOM = [0x7F, 0x10]
    >>>
    >>> apdu = SELECT+DF_TELECOM
    >>> print 'sending ' + toHexString(apdu)
    sending A0 A4 00 00 02 7F 10
    >>> response, sw1, sw2 = cardservice.connection.transmit( apdu, CardConnection.T1_protocol )
    >>> print 'response: ', response, ' status words: ', "%x %x" % (sw1, sw2)
    response: [] status words: 9f 1a
    >>>
    >>> if sw1 == 0x9F:
    ...     GET_RESPONSE = [0XA0, 0XC0, 00, 00 ]
    ...     apdu = GET_RESPONSE + [sw2]
    ...     print 'sending ' + toHexString(apdu)
    ...     response, sw1, sw2 = cardservice.connection.transmit( apdu )
    ...     print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)
    ...
    sending A0 C0 00 00 1A
    response: 00 00 00 00 7F 10 02 00 00 00 00 00 0D 13 00 0A 04 00 83 8A 83 8A 00 01 00 00 status words: 90 0
    >>>

The object-centric approach
===========================

In the object-centric approach, we associate a high-level object with a
set of smart cards supported by the object. For example we associate a
javacard loader class with a set of javacard smart cards. We create a
request for the specific object, and wait until a card supported by the
object is inserted. Once a card supported by the object is inserted, we
perform the required function by calling the objec methods.

To be written...

Tracing APDUs
*************

The brute force
===============

A straightforward way of tracing command and response APDUs is to insert
print statements around the transmit() method calls:

    >>> from smartcard.CardType import ATRCardType
    >>> from smartcard.CardRequest import CardRequest
    >>> from smartcard.util import toHexString, toBytes
    >>>
    >>> cardtype = ATRCardType( toBytes( "3B 16 94 20 02 01 00 00 0D" ) )
    >>> cardrequest = CardRequest( timeout=1, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()
    >>>
    >>> cardservice.connection.connect()
    >>>
    >>> SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    >>> DF_TELECOM = [0x7F, 0x10]
    >>>
    >>> apdu = SELECT+DF_TELECOM
    >>> print 'sending ' + toHexString(apdu)
    sending A0 A4 00 00 02 7F 10
    >>> response, sw1, sw2 = cardservice.connection.transmit( apdu )
    >>> print 'response: ', response, ' status words: ', "%x %x" % (sw1, sw2)
    response: [] status words: 9f 1a
    >>>
    >>> if sw1 == 0x9F:
    ...     GET_RESPONSE = [0XA0, 0XC0, 00, 00 ]
    ...     apdu = GET_RESPONSE + [sw2]
    ...     print 'sending ' + toHexString(apdu)
    ...     response, sw1, sw2 = cardservice.connection.transmit( apdu )
    ...     print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)
    ...
    sending A0 C0 00 00 1A
    response: 00 00 00 00 7F 10 02 00 00 00 00 00 0D 13 00 0A 04 00 83 8A 83 8A 00 01 00 00 status words: 90 0
    >>>

Scripts written this way are quite difficult to read, because there are
more tracing statements than actual apdu transmits..

A small improvement in visibility would be to replace the print
instructions by functions, e.g.:

    >>> from smartcard.CardType import ATRCardType
    >>> from smartcard.CardRequest import CardRequest
    >>> from smartcard.util import toHexString, toBytes
    >>>
    >>> cardtype = ATRCardType( toBytes( "3B 16 94 20 02 01 00 00 0D" ) )
    >>> cardrequest = CardRequest( timeout=1, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()
    >>>
    >>> cardservice.connection.connect()
    >>>
    >>> SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    >>> DF_TELECOM = [0x7F, 0x10]
    >>>
    >>> def trace_command(apdu):
    ...     print 'sending ' + toHexString(apdu)
    ...
    >>> def trace_response( response, sw1, sw2 ):
    ...     if None==response: response=[]
    ...     print 'response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2)
    ...
    >>> apdu = SELECT+DF_TELECOM
    >>> trace_command(apdu)
    sending A0 A4 00 00 02 7F 10
    >>> response, sw1, sw2 = cardservice.connection.transmit( apdu )
    >>> trace_response( response, sw1, sw2 )
    response: status words: 9f 1a
    >>>
    >>> if sw1 == 0x9F:
    ...    GET_RESPONSE = [0XA0, 0XC0, 00, 00 ]
    ...    apdu = GET_RESPONSE + [sw2]
    ...    trace_command(apdu)
    ...    response, sw1, sw2 = cardservice.connection.transmit( apdu )
    ...    trace_response( response, sw1, sw2 )
    ...
    sending A0 C0 00 00 1A
    response: 00 00 00 00 7F 10 02 00 00 00 00 00 0D 13 00 0A 04 00 83 8A 83 8A 00 01 00 00 status words: 90 0
    >>>

Using card connection observers to trace apdu transmission
==========================================================

The prefered solution is to implement a card connection observer, and
register the observer with the card connection. The card connection will
then notify the observer when card connection events occur (e.g.
connection, disconnection, apdu command or apdu response). This is
illustrated in the following script:

    >>> from smartcard.CardType import AnyCardType
    >>> from smartcard.CardRequest import CardRequest
    >>> from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
    >>>
    >>> GET_RESPONSE = [0XA0, 0XC0, 00, 00 ]
    >>> SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    >>> DF_TELECOM = [0x7F, 0x10]
    >>>
    >>>
    >>> cardtype = AnyCardType()
    >>> cardrequest = CardRequest( timeout=10, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()
    >>>
    >>> observer=ConsoleCardConnectionObserver()
    >>> cardservice.connection.addObserver( observer )
    >>>
    >>> cardservice.connection.connect()
    connecting to SchlumbergerSema Reflex USB v.2 0
    >>>
    >>> apdu = SELECT+DF_TELECOM
    >>> response, sw1, sw2 = cardservice.connection.transmit( apdu )
    > A0 A4 00 00 02 7F 10
    < [] 9F 1A
    >>> if sw1 == 0x9F:
    ...     apdu = GET_RESPONSE + [sw2]
    ...     response, sw1, sw2 = cardservice.connection.transmit( apdu )
    ... else:
    ...     print 'no DF_TELECOM'
    ...
    > A0 C0 00 00 1A
    < 00 00 00 00 7F 10 02 00 00 00 00 00 0D 13 00 0A 04 00 83 8A 83 8A 00 01 00 00 90 0
    >>>

In this script, a `ConsoleCardConnectionObserver
<http://pyscard.sourceforge.net/epydoc/smartcard.CardConnectionObserver.ConsoleCardConnectionObserver-class.html>`_
is attached to the card service connection once the watiforcard() call
returns.

    >>> observer=ConsoleCardConnectionObserver()
    >>> cardservice.connection.addObserver( observer )

On card connection events (connect, disconnect, transmit command apdu,
receive response apdu), the card connection notifies its obersers with a
`CarConnectionEvent
<http://pyscard.sourceforge.net/epydoc/smartcard.CardConnectionEvent.CardConnectionEvent-class.html>`_
including the event type and the event data. The
`ConsoleCardConnectionObserver
<http://pyscard.sourceforge.net/epydoc/smartcard.CardConnectionObserver.ConsoleCardConnectionObserver-class.html>`_
is a simple observer that will print on the console the card connection
events. The class definition is the following:

.. sourcecode:: python

    class ConsoleCardConnectionObserver( CardConnectionObserver ):
        def update( self, cardconnection, ccevent ):

            if 'connect'==ccevent.type:
                print 'connecting to ' + cardconnection.getReader()

            elif 'disconnect'==ccevent.type:
                print 'disconnecting from ' + cardconnection.getReader()

            elif 'command'==ccevent.type:
                print '> ', toHexString( ccevent.args[0] )

            elif 'response'==ccevent.type:
                if []==ccevent.args[0]:
                    print '< [] ', "%-2X %-2X" % tuple(ccevent.args[-2:])
                else:
            print '< ', toHexString(ccevent.args[0]), "%-2X %-2X" % tuple(ccevent.args[-2:])

The console card connection observer is thus printing the connect,
disconnect, command and response apdu events:

    >>> cardservice.connection.connect()
    connecting to SchlumbergerSema Reflex USB v.2 0
    >>>
    >>> apdu = SELECT+DF_TELECOM
    >>> response, sw1, sw2 = cardservice.connection.transmit( apdu )
    > A0 A4 00 00 02 7F 10
    < [] 9F 1A
    >>> if sw1 == 0x9F:
    ...     apdu = GET_RESPONSE + [sw2]
    ...     response, sw1, sw2 = cardservice.connection.transmit( apdu )
    ... else:
    ...     print 'no DF_TELECOM'
    ...
    > A0 C0 00 00 1A
    < 00 00 00 00 7F 10 02 00 00 00 00 00 0D 13 00 0A 04 00 83 8A 83 8A 00 01 00 00 90 0

A card connection observer's update methode is called upon card
connection event, with the connection and the connection event as
parameters. The `CardConnectionEvent
<http://pyscard.sourceforge.net/epydoc/smartcard.CardConnectionEvent.CardConnectionEvent-class.html>`_
class definition is the following:

.. sourcecode:: python

    class CardConnectionEvent:
        """Base class for card connection events.

       This event is notified by CardConnection objects.

       type: 'connect', 'disconnect', 'command', 'response'
       args: None for 'connect' or 'disconnect'
       command APDU byte list for 'command'
       [response data, sw1, sw2] for 'response'
       type: 'connect' args:"""
       def __init__( self, type, args=None):
           self.type=type
           self.args=args

You can write your own card connection observer, for example to perform
fancy output in a wxWindows frame, or apdu interpretation. The following
scripts defines a small SELECT and GET RESPONSE apdu interpreter:

    >>> from smartcard.CardType import AnyCardType
    >>> from smartcard.CardRequest import CardRequest
    >>> from smartcard.CardConnectionObserver import CardConnectionObserver
    >>> from smartcard.util import toHexString
    >>>
    >>> from string import replace
    >>>
    >>> class TracerAndSELECTInterpreter( CardConnectionObserver ):
    ...     def update( self, cardconnection, ccevent ):
    ...         if 'connect'==ccevent.type:
    ...             print 'connecting to ' + cardconnection.getReader()
    ...         elif 'disconnect'==ccevent.type:
    ...             print 'disconnecting from ' + cardconnection.getReader()
    ...         elif 'command'==ccevent.type:
    ...             str=toHexString(ccevent.args[0])
    ...             str = replace( str , "A0 A4 00 00 02", "SELECT" )
    ...             str = replace( str , "A0 C0 00 00", "GET RESPONSE" )
    ...             print '> ', str
    ...         elif 'response'==ccevent.type:
    ...             if []==ccevent.args[0]:
    ...                 print '< [] ', "%-2X %-2X" % tuple(ccevent.args[-2:])
    ...             else:
    ...                 print '< ', toHexString(ccevent.args[0]), "%-2X %-2X" % tuple(ccevent.args[-2:])
    ...
    >>>
    >>> GET_RESPONSE = [0XA0, 0XC0, 00, 00 ]
    >>> SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    >>> DF_TELECOM = [0x7F, 0x10]
    >>>
    >>>
    >>> cardtype = AnyCardType()
    >>> cardrequest = CardRequest( timeout=10, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()
    >>>
    >>> observer=TracerAndSELECTInterpreter()
    >>> cardservice.connection.addObserver( observer )
    >>>
    >>> cardservice.connection.connect()
    connecting to SchlumbergerSema Reflex USB v.2 0
    >>>
    >>> apdu = SELECT+DF_TELECOM
    >>> response, sw1, sw2 = cardservice.connection.transmit( apdu )
    > SELECT 7F 10
    < [] 9F 1A
    >>> if sw1 == 0x9F:
    ...     apdu = GET_RESPONSE + [sw2]
    ...     response, sw1, sw2 = cardservice.connection.transmit( apdu )
    ... else:
    ...     print 'no DF_TELECOM'
    ...
    > GET RESPONSE 1A
    < 00 00 00 00 7F 10 02 00 00 00 00 00 0D 13 00 0A 04 00 83 8A 83 8A 00 01 00 00 90 0
    >>>

Testing for APDU transmission errors
************************************

Upon transmission and processing of an APDU, the smart card returns a
pair of status words, SW1 and SW2, to report various success or error
codes following the required processing. Some of these success or error
codes are standardized in ISO7816-4, ISO7816-8 or ISO7816-9, for
example. Other status word codes are standardized by standardization
bodies such as Open Platform (e.g. javacard), 3GPP (e.g. SIM or USIM
cards), or Eurocard-Mastercard-Visa (EMV) (e.g. banking cards). Finally,
any smart card application developper can defined application related
proprietary codes; for example the MUSCLE applet defines a set of
prioprietary codes related to the MUSCLE applet features.

Some of these status word codes are uniques, but others have a different
meaning depending on the card type and its supported standards. For
example, ISO7816-4 defines the error code 0x62 0x82 as "File
Invalidated", whereas in Open Platform 2.1 the same error code is
defined as "Card life cycle is CARD_LOCKED". As a result, the list of
error codes that can be returned by a smart card and they interpretation
depend on the card type. The following discussion outlines possible
strategies to check and report smart card status word errors.

The brute force for testing APDU transmission errors
====================================================

As for APDU tracing, a straightforward way of checking for errors in response APDUs during the execution of scripts is to insert testt statements after the transmit() method calls:

    >>> from smartcard.CardType import AnyCardType
    >>> from smartcard.CardRequest import CardRequest
    >>> from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
    >>>
    >>> GET_RESPONSE = [0XA0, 0XC0, 00, 00 ]
    >>> SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    >>> DF_TELECOM = [0x7F, 0x10]
    >>>
    >>> cardtype = AnyCardType()
    >>> cardrequest = CardRequest( timeout=10, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()
    >>>
    >>> observer=ConsoleCardConnectionObserver()
    >>> cardservice.connection.addObserver( observer )
    >>>
    >>> cardservice.connection.connect()
    connecting to Utimaco CardManUSB 0
    >>>
    >>> apdu = SELECT+DF_TELECOM
    >>> response, sw1, sw2 = cardservice.connection.transmit( apdu )
    > A0 A4 00 00 02 7F 10
    < [] 6E 0
    >>>
    >>> if sw1 in range(0x61, 0x6f):
    ... print "Error: sw1: %x sw2: %x" % (sw1, sw2)
    ...
    Error: sw1: 6e sw2: 0
    >>> if sw1 == 0x9F:
    ... apdu = GET_RESPONSE + [sw2]
    ... response, sw1, sw2 = cardservice.connection.transmit( apdu )
    ...
    >>> cardservice.connection.disconnect()
    disconnecting from Utimaco CardManUSB 0
    >>>

Scripts written this way are quite difficult to read, because there are
more error detection statements than actual apdu transmits.

An improvement in visibility is to wrap the transmit instruction inside
a function mytransmit, e.g.:

    >>> from smartcard.CardType import AnyCardType
    >>> from smartcard.CardRequest import CardRequest
    >>> from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
    >>>
    >>> def mytransmit( connection, apdu ):
    ... response, sw1, sw2 = connection.transmit( apdu )
    ... if sw1 in range(0x61, 0x6f):
    ... print "Error: sw1: %x sw2: %x" % (sw1, sw2)
    ... return response, sw1, sw2
    ...
    >>>
    >>> GET_RESPONSE = [0XA0, 0XC0, 00, 00 ]
    >>> SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    >>> DF_TELECOM = [0x7F, 0x10]
    >>>
    >>>
    >>> cardtype = AnyCardType()
    >>> cardrequest = CardRequest( timeout=10, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()
    >>>
    >>> observer=ConsoleCardConnectionObserver()
    >>> cardservice.connection.addObserver( observer )
    >>>
    >>> cardservice.connection.connect()
    connecting to Utimaco CardManUSB 0
    >>>
    >>> apdu = SELECT+DF_TELECOM
    >>> response, sw1, sw2 = mytransmit( cardservice.connection, apdu )
    > A0 A4 00 00 02 7F 10
    < [] 6E 0
    Error: sw1: 6e sw2: 0
    >>>
    >>> if sw1 == 0x9F:
    ... apdu = GET_RESPONSE + [sw2]
    ... response, sw1, sw2 = mytransmit( cardservice.connection, apdu )
    ...
    >>> cardservice.connection.disconnect()
    disconnecting from Utimaco CardManUSB 0
    >>>

The prefered solution is for testing errors is to use
smarcard.sw.ErrorChecker, as described in the following section.

Checking APDU transmission errors with error checkers
=====================================================

Status word errors can occur from different sources. The ISO7816-4
standards defines status words for sw1 in the range 0x62 to 0x6F and
some values of sw2, except for 0x66 which is reserved for security
related issues. The ISO7816-8 standards define other status words, e.g.
sw1=0x68 and sw2=0x83 or 0x84 for command chaining errors. Other
standards, like Open Platform, define additional status words error,
e.g. sw1=0x94 and sw2=0x84.

The prefered strategy for status word error checking is based around
individual error checkers (smartcard.sw.ErrorChecker) that can be
chained into an error checking chain (smartcars.sw.ErrorCheckingChain).

Error checkers
--------------

An error checker is a class deriving from `ErrorChecker
<http://pyscard.sourceforge.net/epydoc/smartcard.sw.ErrorChecker.ErrorChecker-class.html>`_
that checks for recognized sw1, sw2 error conditions when called, and
raises an exception when finding such condition. This is illustrated in
the following sample:

    >>> from smartcard.sw.ISO7816_4ErrorChecker import ISO7816_4ErrorChecker
    >>>
    >>> errorchecker=ISO7816_4ErrorChecker()
    >>> errorchecker( [], 0x90, 0x00 )
    >>> errorchecker( [], 0x6A, 0x80 )
    Traceback (most recent call last):
    File "<stdin>", line 1, in ?
    File "D:\projects\pyscard-install\factory\python\lib\site-packages\smartcard\sw\ISO7816_4ErrorChecker.py", line 137, in __call__
    raise exception( data, sw1, sw2, message )
    smartcard.sw.SWExceptions.CheckingErrorException: 'Status word exception: checking error - Incorrect parameters in the data field!'
    >>>

The first call to error checker does not raise an exception, since 90 00
does not report any error. The second calls however raises a
CheckingErrorException.

Error checking chains
---------------------

Error checkers can be chained into `error checking chain
<http://pyscard.sourceforge.net/epydoc/smartcard.sw.ErrorCheckingChain.ErrorCheckingChain-class.html>`_.
Each checker in the chain is called until an error condition is met, in
which case an exception is raised. This is illustrated in the following
sample:

    >>> from smartcard.sw.ISO7816_4ErrorChecker import ISO7816_4ErrorChecker
    >>> from smartcard.sw.ISO7816_8ErrorChecker import ISO7816_8ErrorChecker
    >>> from smartcard.sw.ISO7816_9ErrorChecker import ISO7816_9ErrorChecker
    >>>
    >>> from smartcard.sw.ErrorCheckingChain import ErrorCheckingChain
    >>>
    >>> errorchain = []
    >>> errorchain=[ ErrorCheckingChain( errorchain, ISO7816_9ErrorChecker() ),
    ... ErrorCheckingChain( errorchain, ISO7816_8ErrorChecker() ),
    ... ErrorCheckingChain( errorchain, ISO7816_4ErrorChecker() ) ]
    >>>
    >>> errorchain[0]( [], 0x90, 0x00 )
    >>> errorchain[0]( [], 0x6A, 0x8a )
    Traceback (most recent call last):
    File "<stdin>", line 1, in ?
    File "D:\projects\pyscard-install\factory\python\lib\site-packages\smartcard\sw\ErrorCheckingChain.py", line 60,
    in __call__
    self.strategy( data, sw1, sw2 )
    File "D:\projects\pyscard-install\factory\python\lib\site-packages\smartcard\sw\ISO7816_9ErrorChecker.py", line 74, in __call__
    raise exception( data, sw1, sw2, message )
    smartcard.sw.SWExceptions.CheckingErrorException: 'Status word exception: checking error - DF name already exists!'
    >>>

In this sample, an error checking chain is created that will check first
for iso 7816-9 errors, then iso7816-8 errors, and finally iso7816-4
errors.

The first call to the error chain does not raise an exception, since 90
00 does not report any error. The second calls however raises a
CheckingErrorException, caused by the iso7816-9 error checker.

Filtering exceptions
--------------------

You can filter undesired exceptions in a chain by adding a filtered
exception to the error checking chain::

    >>> from smartcard.sw.ISO7816_4ErrorChecker import ISO7816_4ErrorChecker
    >>> from smartcard.sw.ISO7816_8ErrorChecker import ISO7816_8ErrorChecker
    >>> from smartcard.sw.ISO7816_9ErrorChecker import ISO7816_9ErrorChecker
    >>>
    >>> from smartcard.sw.ErrorCheckingChain import ErrorCheckingChain
    >>>
    >>> errorchain = []
    >>> errorchain=[ ErrorCheckingChain( errorchain, ISO7816_9ErrorChecker() ),
    ... ErrorCheckingChain( errorchain, ISO7816_8ErrorChecker() ),
    ... ErrorCheckingChain( errorchain, ISO7816_4ErrorChecker() ) ]
    >>>
    >>>
    >>> errorchain[0]( [], 0x90, 0x00 )
    >>> errorchain[0]( [], 0x62, 0x00 )
    Traceback (most recent call last):
    File "<stdin>", line 1, in ?
    File "D:\projects\pyscard-install\factory\python\lib\site-packages\smartcard\sw\ErrorCheckingChain.py", line 72, in __call__
    return self.next()( data, sw1, sw2 )
    File "D:\projects\pyscard-install\factory\python\lib\site-packages\smartcard\sw\ErrorCheckingChain.py", line 72, in __call__
    return self.next()( data, sw1, sw2 )
    File "D:\projects\pyscard-install\factory\python\lib\site-packages\smartcard\sw\ErrorCheckingChain.py", line 60, in __call__
    self.strategy( data, sw1, sw2 )
    File "D:\projects\pyscard-install\factory\python\lib\site-packages\smartcard\sw\ISO7816_4ErrorChecker.py", line 137, in __call__
    raise exception( data, sw1, sw2, message )
    smartcard.sw.SWExceptions.WarningProcessingException: 'Status word exception: warning processing - Response padded/ More APDU commands expected!'
    >>>
    >>> from smartcard.sw.SWExceptions import WarningProcessingException
    >>>
    >>> errorchain[0].addFilterException( WarningProcessingException )
    >>> errorchain[0]( [], 0x62, 0x00 )
    >>>

The first call to the error chain with sw1 sw2 = 62 00 raises a
`WarningProcessingException
<http://pyscard.sourceforge.net/epydoc/smartcard.sw.SWExceptions.WarningProcessingException-class.html>`_.

::

    ...
    >>> errorchain[0]( [], 0x62, 0x00 )
    Traceback (most recent call last):
    ...

After adding a filter for `WarningProcessingException
<http://pyscard.sourceforge.net/epydoc/smartcard.sw.SWExceptions.WarningProcessingException-class.html>`_,
the second call to the error chain with sw1 sw2 = 62 00 does not raise
any exception:

    >>> from smartcard.sw.SWExceptions import WarningProcessingException
    >>>
    >>> errorchain[0].addFilterException( WarningProcessingException )
    >>> errorchain[0]( [], 0x62, 0x00 )
    >>>

Detecting response APDU errors for a card connection
----------------------------------------------------

To detect APDU response errors during transmission, simply set the error checking chain of the connection used for transmission:

::

    from smartcard.CardType import AnyCardType
    from smartcard.CardRequest import CardRequest
    from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver

    from smartcard.sw.ErrorCheckingChain import ErrorCheckingChain
    from smartcard.sw.ISO7816_4ErrorChecker import ISO7816_4ErrorChecker
    from smartcard.sw.ISO7816_8ErrorChecker import ISO7816_8ErrorChecker
    from smartcard.sw.SWExceptions import SWException, WarningProcessingException

    # request any card
    cardtype = AnyCardType()
    cardrequest = CardRequest( timeout=10, cardType=cardtype )
    cardservice = cardrequest.waitforcard()

    # our error checking chain
    errorchain=[]
    errorchain=[ ErrorCheckingChain( errorchain, ISO7816_8ErrorChecker() ),
                 ErrorCheckingChain( errorchain, ISO7816_4ErrorChecker() ) ]
    cardservice.connection.setErrorCheckingChain( errorchain )

    # a console tracer
    observer=ConsoleCardConnectionObserver()
    cardservice.connection.addObserver( observer )

    # send a few apdus; exceptions will occur upon errors
    cardservice.connection.connect()

    try:
        SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
        DF_TELECOM = [0x7F, 0x10]
        apdu = SELECT+DF_TELECOM
        response, sw1, sw2 = cardservice.connection.transmit( apdu )
        if sw1 == 0x9F:
            GET_RESPONSE = [0XA0, 0XC0, 00, 00 ]
            apdu = GET_RESPONSE + [sw2]
            response, sw1, sw2 = cardservice.connection.transmit( apdu )
    except SWException, e:
        print str(e)


Executing the previous script on a SIM card will cause an output similar to:

::

    connecting to SchlumbergerSema Reflex USB v.2 0
    > A0 A4 00 00 02 7F 10
    < [] 9F 1A
    > A0 C0 00 00 1A
    < 00 00 00 00 7F 10 02 00 00 00 00 00 0D 13 00 0A 04 00 83 8A 83 8A 00 01 00 00 90 0
    disconnecting from SchlumbergerSema Reflex USB v.2 0
    disconnecting from SchlumbergerSema Reflex USB v.2 0

whereas executing the script on a non-SIM card will result in:

::

    connecting to Utimaco CardManUSB 0
    > A0 A4 00 00 02 7F 10
    < [] 6E 0
    'Status word exception: checking error - Class (CLA) not supported!'
    disconnecting from Utimaco CardManUSB 0
    disconnecting from Utimaco CardManUSB 0

To implement an error checking chain, create an `ErrorCheckingChain
<http://pyscard.sourceforge.net/epydoc/smartcard.sw.ErrorCheckingChain.ErrorCheckingChain-class.html>`_
object with the desired error checking strategies, and set this chain
object as the card connection error checking chain. The card connection
will use the chain for error checking upon reception of a response apdu:

Writing a custom error checker
------------------------------

Implementing a custom error checker requires implementing a sub-class of
`op21_ErrorChecker
<http://pyscard.sourceforge.net/epydoc/smartcard.sw.op21_ErrorChecker.op21_ErrorChecker-class.html>`_,
and overriding the __call__ method. The following error checker raises a
`SecurityRelatedException
<http://pyscard.sourceforge.net/epydoc/smartcard.sw.SWExceptions.SecurityRelatedException-class.html>`_
exception when sw1=0x66 and sw2=0x00:

.. sourcecode:: python

    from smartcard.sw.ErrorChecker import ErrorChecker
    from smartcard.sw.SWExceptions import SecurityRelatedException

    class MyErrorChecker( ErrorChecker ):
        def __call__( self, data, sw1, sw2 ):
            if 0x66==sw1 and 0x00==sw2:
                raise SecurityRelatedException( data, sw1, sw2 )

    Custom checkers can be used standalone, as in the following sample, or chained to other error checkers:

    from smartcard.CardType import AnyCardType
    from smartcard.CardRequest import CardRequest

    from smartcard.sw.ErrorCheckingChain import ErrorCheckingChain
    from smartcard.sw.ErrorChecker import ErrorChecker
    from smartcard.sw.SWExceptions import SecurityRelatedException

    class MyErrorChecker( ErrorChecker ):
        def __call__( self, data, sw1, sw2 ):
            if 0x66==sw1 and 0x00==sw2:
                raise SecurityRelatedException( data, sw1, sw2 )

    # request any card
    cardtype = AnyCardType()
    cardrequest = CardRequest( timeout=10, cardType=cardtype )
    cardservice = cardrequest.waitforcard()

    # our error checking chain
    errorchain=[]
    errorchain=[ ErrorCheckingChain( [], MyErrorChecker() ) ]
    cardservice.connection.setErrorCheckingChain( errorchain )

    # send a few apdus; exceptions will occur upon errors
    cardservice.connection.connect()

    SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    DF_TELECOM = [0x7F, 0x10]
    apdu = SELECT+DF_TELECOM
    response, sw1, sw2 = cardservice.connection.transmit( apdu )
    if sw1 == 0x9F:
        GET_RESPONSE = [0XA0, 0XC0, 00, 00 ]
        apdu = GET_RESPONSE + [sw2]
        response, sw1, sw2 = cardservice.connection.transmit( apdu )


Smartcard readers
*****************

Listing Smartcard Readers
=========================

The easiest way to retrieve the list of smartcard readers is the
smartcard.System.readers() function:

    >>> import smartcard.System
    >>> print smartcard.System.readers()
    ['Schlumberger e-gate 0', 'SchlumbergerSema Reflex USB v.2 0', 'Utimaco CardManUSB 0']
    >>>

Organizing Smartcard Readers into reader groups
===============================================

Reader group management is only available on Windows, since PCSC-lite
does not currently supports reader groups management.

Readers can be organized in reader groups. To retrieve the smartcard
reader groups, use readergroups():

    >>> import smartcard.System
    >>> print smartcard.System.readergroups()
    ['SCard$DefaultReaders']
    >>>

The readergroups() object has all the list attributes. To add a reader
group, simply use the + operator, e.g.:

    >>> from smartcard.System import readergroups
    >>> g=readergroups()
    >>> print g
    ['SCard$DefaultReaders']
    >>> g+='Biometric$Readers'
    >>> print g
    ['SCard$DefaultReaders', 'Biometric$Readers']
    >>>

You can also use the append and insert methods, as well as the + operator, e.g.:

    >>> from smartcard.System import readergroups
    >>> g=readergroups()
    >>> print g
    ['SCard$DefaultReaders']
    >>> g=g+['Biometric$Readers','Pinpad$Readers']
    >>> print g
    ['SCard$DefaultReaders', 'Biometric$Readers', 'Pinpad$Readers']
    >>>

or

    >>> from smartcard.System import readergroups
    >>> g=readergroups()
    >>> print g
    ['SCard$DefaultReaders']
    >>> g.append('Biometric$Readers')
    >>> g.insert(1,'Pinpad$Readers')
    >>> print g
    ['SCard$DefaultReaders', 'Pinpad$Readers', 'Biometric$Readers']
    >>>

Smartcard reader groups are not persistent until a reader as been added
to the group. To add a reader to a reader group, use
addreadertogroups():

    >>> from smartcard.System import readergroups, addreadertogroups, readers
    >>> g=readergroups()
    >>> g+='USB$Readers'
    >>> addreadertogroups( 'Schlumberger e-gate 0', 'USB$Readers' )
    >>> readers( 'USB$Readers')
    ['Schlumberger e-gate 0']
    >>>

To remove a reader group, all list operators are available to manage
reader groups, including pop() or remove():

    >>> from smartcard.System import readergroups, addreadertogroups, readers
    >>> g=readergroups()
    >>> g+='USB$Readers'
    >>> print g
    ['SCard$DefaultReaders', 'USB$Readers']
    >>> g.pop(1)
    'USB$Readers'
    >>> g
    ['SCard$DefaultReaders']
    >>>

or

    >>> from smartcard.System import readergroups, addreadertogroups, readers
    >>> g=readergroups()
    >>> g+='USB$Readers'
    >>> print g
    ['SCard$DefaultReaders', 'USB$Readers']
    >>> readergroups().remove('USB$Readers')
    >>> readergroups()
    ['SCard$DefaultReaders']
    >>>

Monitoring readers
==================

You can monitor the insertion or removal of readers using the
`ReaderObserver
<http://pyscard.sourceforge.net/epydoc/smartcard.ReaderMonitoring.ReaderObserver-class.html>`_
interface.

To monitor reader insertion, create a `ReaderObserver
<http://pyscard.sourceforge.net/epydoc/smartcard.ReaderMonitoring.ReaderObserver-class.html>`_
object that implements an update() method that will be called upon
reader/insertion removal. The following sample code implements a
ReaderObserver that simply prints the inserted/removed readers on the
standard output:

.. sourcecode:: python

    from smartcard.ReaderMonitoring import ReaderObserver

    class printobserver( ReaderObserver ):
        """A simple reader observer that is notified
        when readers are added/removed from the system and
        prints the list of readers
        """
        def update( self, observable, (addedreaders, removedreaders) ):
            print "Added readers", addedreaders
            print "Removed readers", removedreaders
  

To monitor reader insertion/removal, simply add the observer to the
`ReaderMonitor
<http://pyscard.sourceforge.net/epydoc/smartcard.ReaderMonitoring.ReaderMonitor-class.html>`_:

.. sourcecode:: python

    from sys import stdin, exc_info
    from time import sleep

    from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver

    try:
        print "Add or remove a smartcard reader to the system."
        print "This program will exit in 10 seconds"
        print ""
        readermonitor = ReaderMonitor()
        readerobserver = printobserver()
        readermonitor.addObserver( readerobserver )

        sleep(10)

        # don't forget to remove observer, or the
        # monitor will poll forever...
        readermonitor.deleteObserver(readerobserver)

        print 'press Enter to continue'
        stdin.readline()

    except error:
        print exc_info()[0], ': ', exc_info()[1]

Smart Cards
***********

Monitoring Smart Cards
======================

You can monitor the insertion or removal of cards using the
`CardObserver
<http://pyscard.sourceforge.net/epydoc/smartcard.CardMonitoring.CardObserver-class.html>`_
interface.

To monitor card insertion and removal, create a `CardObserver
<http://pyscard.sourceforge.net/epydoc/smartcard.CardMonitoring.CardObserver-class.html>`_
object that implements an update() method that will be called upon card
insertion/removal. The following sample code implements a CardObserver
that simply prints the inserted/removed cards on the standard output,
named printobserver. To monitor card insertion/removal, simply add the
card observer to the `CardMonitor
<http://pyscard.sourceforge.net/epydoc/smartcard.CardMonitoring.CardMonitor-class.html>`_:

.. sourcecode:: python

    from smartcard.CardMonitoring import CardMonitor, CardObserver
    from smartcard.util import *

    # a simple card observer that prints inserted/removed cards
    class printobserver( CardObserver ):
        """A simple card observer that is notified
        when cards are inserted/removed from the system and
        prints the list of cards
        """
        def update( self, observable, (addedcards, removedcards) ):
            for card in addedcards:
                print "+Inserted: ", toHexString( card.atr )
            for card in removedcards:
                print "-Removed: ", toHexString( card.atr )

    try:
        print "Insert or remove a smartcard in the system."
        print "This program will exit in 10 seconds"
        print ""
        cardmonitor = CardMonitor()
        cardobserver = printobserver()
        cardmonitor.addObserver( cardobserver )


Sending APDUs to a Smart Card Obtained from Card Monitoring
===========================================================

The update method of the CardObserver receives two lists of Cards
objects, the recently added cards and the recently removed cards. A
connection can be created to each Card object of the added card list for
sending APDUS.

The following sample code implements a CardObserver class named
transmitobserver, that connects to inserted cards and transmit an APDU,
in our case SELECT DF_TELECOM:

.. sourcecode:: python

    # a card observer that connects to new cards and performs a transaction, e.g. SELECT DF_TELECOM
    class transmitobserver( CardObserver ):
        """A card observer that is notified when cards are inserted/removed from the system,
        connects to cards and SELECT DF_TELECOM
        """
        def __init__( self ):
            self.cards=[]

        def update( self, observable, (addedcards, removedcards) ):
            for card in addedcards:
                if card not in self.cards:
                    self.cards+=[card]
                    print "+Inserted: ", toHexString( card.atr )
                    card.connection = card.createConnection()
                    card.connection.connect()
                    response, sw1, sw2 = card.connection.transmit( SELECT_DF_TELECOM )
                    print "%.2x %.2x" % (sw1, sw2)

            for card in removedcards:
                print "-Removed: ", toHexString( card.atr )
                if card in self.cards:
                    self.cards.remove( card )


To monitor card insertion, connect to inserted cards and send the APDU,
create an instance of transmitobserver and add it to the `CardMonitor
<http://pyscard.sourceforge.net/epydoc/smartcard.CardMonitoring.CardMonitor-class.html>`_:

.. sourcecode:: python

    from time import sleep
    print "Insert or remove a smartcard in the system."
    print "This program will exit in 100 seconds"
    print ""
    cardmonitor = CardMonitor()
    cardobserver = transmitobserver()
    cardmonitor.addObserver( cardobserver )

    sleep(100)

Connections
***********

Connecting to a card and sending APDUs is done thru a CardConnection
object. CardConnection objects are created using a CardRequest, or by
the CardMonitoring.

Creating a Connection from a CardRequest
========================================

A successful CardRequest returns a CardService matching the requested
card service for the card, or a PassThruCardService if no specific card
service was required:

    >>> from smartcard.CardType import AnyCardType
    >>> from smartcard.CardRequest import CardRequest
    >>> from smartcard.util import toHexString
    >>>
    >>> cardtype = AnyCardType()
    >>> cardrequest = CardRequest( timeout=1, cardType=cardtype )
    >>> cardservice = cardrequest.waitforcard()
    >>>
    >>> cardservice.connection.connect()
    >>> print toHexString( cardservice.connection.getATR() )
    3B 16 94 20 02 01 00 00 0D
    >>> print cardservice.connection.getReader()
    SchlumbergerSema Reflex USB v.2 0

Each CardService has a connection attribute, which is a CardConnection
for the card.

Creating Connection from CardMonitoring
=======================================

The `update
<http://pyscard.sourceforge.net/pyscard-usersguide.html#monitoringsmartcards>`_
method of a CardObserver receives a tuple with a list of connected cards
and a list of removed cards. To create a CardConnection from a card
object, use the createConnection() method of the desired card:

.. sourcecode:: python

    class myobserver( CardObserver ):
        def update( self, observable, (addedcards, removedcards) ):
            for card in addedcards:
                    print "+Inserted: ", toHexString( card.atr )
                    card.connection = card.createConnection()
                    card.connection.connect()
                    response, sw1, sw2 = card.connection.transmit( SELECT_DF_TELECOM )
                    print "%.2x %.2x" % (sw1, sw2)


Card Connection Decorators
==========================

APDUs are transmitted to a card using the CardConnection object. It is
sometime useful to change transparently the behaviour of a smart card
connection, for example to establish automatically a secure channel, or
filter and modify on the fly some APDU commands or responses, or the
smart card ATR. pyscard uses theDecorator design pattern to dynamically
change the behaviour of a smart card connection. A
CardConnectionDecorator modifies the behaviour of a CardConnection
object. For example, the following CardConnectionDecorator overwrites
the CardConnection getATR() method:

.. sourcecode:: python

    class FakeATRConnection( CardConnectionDecorator ):
        '''This decorator changes the fist byte of the ATR.'''
        def __init__( self, cardconnection ):
            CardConnectionDecorator.__init__( self, cardconnection )

        def getATR( self ):
            """Replace first BYTE of ATR by 3F"""
            atr = CardConnectionDecorator.getATR( self )
            return [ 0x3f ] + atr [1:]


To apply the decorator, just construct the decorator around the
CardConnection instance to wrap and use the decorator in place of the
card connection object:

.. sourcecode:: python

    # request any card type
    cardtype = AnyCardType()
    cardrequest = CardRequest( timeout=1.5, cardType=cardtype )
    cardservice = cardrequest.waitforcard()

    # attach the console tracer
    observer=ConsoleCardConnectionObserver()
    cardservice.connection.addObserver( observer )

    # attach our decorator
    cardservice.connection = FakeATRConnection( cardservice.connection )

    # connect to the card and perform a few transmits
    cardservice.connection.connect()

    print 'ATR', toHexString( cardservice.connection.getATR() )


Decorators can be nested. For example to nest a FakeATRConnection with a
SecureChannelConnection, use the following construction:


.. sourcecode:: python

    # attach our decorator
    FakeATRConnection( SecureChannelConnection( cardservice.connection ) )

    # connect to the card and perform a few transmits
    cardservice.connection.connect()

    print 'ATR', toHexString( cardservice.connection.getATR() )


Exclusive Card Connection Decorator
-----------------------------------

The ExclusiveConnectCardConnection object performs an exclusive
connection to the card, i.e. no other thread or process will be able to
connect to the card. With PCSC readers, this is done by performing a
SCardConnect with the SCARD_SHARE_EXCLUSIVE attribute.

.. sourcecode:: python

    from smartcard.CardType import AnyCardType
    from smartcard.CardRequest import CardRequest
    from smartcard.CardConnection import CardConnection
    from smartcard.util import toHexString

    from smartcard.ExclusiveConnectCardConnection import ExclusiveConnectCardConnection

    # request any card type
    cardtype = AnyCardType()
    cardrequest = CardRequest( timeout=5, cardType=cardtype )
    cardservice = cardrequest.waitforcard()

    # attach our decorator
    cardservice.connection = ExclusiveConnectCardConnection( cardservice.connection )

    # connect to the card and perform a few transmits
    cardservice.connection.connect()

    print 'ATR', toHexString( cardservice.connection.getATR() )

Exclusive Transmit Card Connection Decorator
--------------------------------------------

The ExclusiveTransmitCardConnection performs an exclusive transaction to
the card, i.e. a series of transmit that cannot be interupted by other
threads' transmits. To do so, include the desired transmits between an
lock() and unlock() method call on the ExclusiveTransmitCardConnection:

.. sourcecode:: python

    from smartcard.CardType import AnyCardType
    from smartcard.CardRequest import CardRequest
    from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
    from smartcard.CardConnection import CardConnection
    from smartcard.util import toHexString

    from smartcard.ExclusiveTransmitCardConnection import ExclusiveTransmitCardConnection


    # define the apdus used in this script
    GET_RESPONSE = [0XA0, 0XC0, 00, 00 ]
    SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    DF_TELECOM = [0x7F, 0x10]

    # request any card type
    cardtype = AnyCardType()
    cardrequest = CardRequest( timeout=5, cardType=cardtype )
    cardservice = cardrequest.waitforcard()

    # attach the console tracer
    observer=ConsoleCardConnectionObserver()
    cardservice.connection.addObserver( observer )

    # attach our decorator
    cardservice.connection = ExclusiveTransmitCardConnection( cardservice.connection )

    # connect to the card and perform a few transmits
    cardservice.connection.connect()

    print 'ATR', toHexString( cardservice.connection.getATR() )

    try:
        # lock for initiating transaction
        cardservice.connection.lock()

        apdu = SELECT+DF_TELECOM
        response, sw1, sw2 = cardservice.connection.transmit( apdu )

        if sw1 == 0x9F:
            apdu = GET_RESPONSE + [sw2]
            response, sw1, sw2 = cardservice.connection.transmit( apdu )
    finally:
        # unlock connection at the end of the transaction
        cardservice.connection.unlock()


Secure Channel Card Connection Decorator
----------------------------------------

Another sample of application of CardConnection decorators is to
implement secure channel. The following sample is a template
CardConnection decorator for secure channel, where each command APDU is
cyphered and each response APDU is uncyphered:

.. sourcecode:: python

    class SecureChannelConnection( CardConnectionDecorator ):
        '''This decorator is a mockup of secure channel connection.
        It merely pretends to cypher/uncypher upon apdu transmission.'''
        def __init__( self, cardconnection ):
            CardConnectionDecorator.__init__( self, cardconnection )

        def cypher( self, bytes ):
            '''Cypher mock-up; you would include the secure channel logics here.'''
            print 'cyphering', toHexString( bytes )
            return bytes

        def uncypher( self, data ):
            '''Uncypher mock-up; you would include the secure channel logics here.'''
            print 'uncyphering', toHexString( data )
            return data

        def transmit( self, bytes, protocol=None ):
            """Cypher/uncypher APDUs before transmission"""
            cypheredbytes = self.cypher( bytes )
            data, sw1, sw2 = CardConnectionDecorator.transmit( self, cypheredbytes, protocol )
            if []!=data:
                data = self.uncypher( data )
            return data, sw1, sw2

A word on cryptography
**********************

Smart card are security devices. As a result, smart card applications
usually require some kind cryptography, for example to establish a
secure channel with the smart card. One of the reference cryptographic
modules for python is `pycrypto
<http://www.amk.ca/python/code/crypto.html>`_, the python cryptographic
toolkit. This section shows briefly the basics of pycrypto to give you a
quick start to include cryptography in you python smart card
applications.

Bynary strings and list of bytes
================================

pycrypto processes binary strings, i.e. python strings that contains
characters such as '\01\42\70\23', whereas pyscard processes APDUs as
list of bytes such as [0x01, 0x42, 0x70, 0x23]. The utility function
HexListToBinString and BinStringToHexList (and their short name versions
hl2bs and bs2hl) provide conversion between the two types.

.. sourcecode:: python

    from smartcard.util import HexListToBinString, BinStringToHexList
    test_data = [ 0x01, 0x42, 0x70, 0x23 ]
    binstring = HexListToBinString( test_data )
    hexlist = BinStringToHexList( binstring )
    print binstring, hexlist
    ?Bp# [1, 66, 112, 35]
    Hashing

pycrypto supports the following hashing algorithms: SHA-1, MD2, MD4 et
MD5. To hash 16 bytes of data with SHA-1:

.. sourcecode:: python

    from Crypto.Hash import SHA

    from smartcard.util import toHexString, PACK

    test_data = [ 0x01, 0x42, 0x70, 0x23 ]
    binstring = HexListToBinString( test_data )

    zhash = SHA.new( binstring )
    hash_as_string = zhash.digest()[:16]
    hash_as_bytes = BinStringToHexList( hash_as_string )
    print hash_as_string, ',', toHexString( hash_as_bytes, PACK )

To perform MD5 hashing, just replace SHA by MD5 in the previous script.

Secret key cryptography
=======================

pycrypto supports several secret key algorithms, such as DES, triple
DES, AES, blowfish, or IDEA. To perform triple DES ciphering in ECB
mode:

.. sourcecode:: python

    from Crypto.Cipher import DES3

    from smartcard.util import toBytes

    key = "31323334353637383132333435363738"
    key_as_binstring = HexListToBinString( toBytes( key ) )
    zdes = DES3.new( key_as_binstring, DES3.MODE_ECB )

    message = "71727374757677787172737475767778"
    message_as_binstring = HexListToBinString( toBytes( message ) )

    encrypted_as_string = zdes.encrypt( message_as_binstring )
    decrypted_as_string = zdes.decrypt( encrypted_as_string )
    print message_as_binstring, encrypted_as_string, decrypted_as_string

