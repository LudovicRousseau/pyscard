# https://github.com/Shayennn/KOBThaiID/blob/master/dump.py

from smartcard.CardType import AnyCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes

cardtype = AnyCardType()
cardrequest = CardRequest( timeout=60, cardType=cardtype )
cardservice = cardrequest.waitforcard()
cardservice.connection.connect(CardConnection.T0_protocol)

SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08]
THAI_ID_CARD = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]
REQ_CID = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]
REQ_THAI_NAME = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0x64]
REQ_ENG_NAME = [0x80, 0xb0, 0x00, 0x75, 0x02, 0x00, 0x64]
REQ_GENDER = [0x80, 0xb0, 0x00, 0xE1, 0x02, 0x00, 0x01]
REQ_DOB = [0x80, 0xb0, 0x00, 0xD9, 0x02, 0x00, 0x08]
REQ_ADDRESS = [0x80, 0xb0, 0x15, 0x79, 0x02, 0x00, 0x64]
REQ_ISSUE_EXPIRE = [0x80, 0xb0, 0x01, 0x67, 0x02, 0x00, 0x12]
REQ_OFFICE=[0x80, 0xB0, 0x00, 0xE2, 0x02, 0x00, 0x64]
REQ_CARD_UNIQUE=[0x80, 0xB0, 0x16, 0x19, 0x02, 0x00, 0x0E]
REQ_OFFICER=[0x80, 0xB0, 0x01, 0x5A, 0x02, 0x00, 0x0D]

DATA = [REQ_CID,REQ_THAI_NAME,REQ_ENG_NAME,REQ_GENDER,REQ_DOB,REQ_ADDRESS,REQ_ISSUE_EXPIRE,REQ_OFFICE,REQ_CARD_UNIQUE,REQ_OFFICER]
apdu = SELECT+THAI_ID_CARD

response, sw1, sw2 = cardservice.connection.transmit( apdu )
response, sw1, sw2 = cardservice.connection.transmit( REQ_CID )
if sw1 == 0x61:
	GET_RESPONSE = [0X00, 0XC0, 0x00, 0x00 ]
	apdu = GET_RESPONSE + [sw2]
	response, sw1, sw2 = cardservice.connection.transmit( apdu )
	result = ""
	for i in response:
		result = result+chr(i)
	f = open(result+'.jpg','w')
	f2 = open(result+'.txt','w')
for d in DATA:
		response, sw1, sw2 = cardservice.connection.transmit( d )
		if sw1 == 0x61:
			GET_RESPONSE = [0X00, 0XC0, 0x00, 0x00 ]
			apdu = GET_RESPONSE + [sw2]
			response, sw1, sw2 = cardservice.connection.transmit( apdu )
			result = ""
			for i in response:
				result = result+chr(i)
			f2.write(result.rstrip().decode('tis-620').encode('utf8')+"\n")
response, sw1, sw2 = cardservice.connection.transmit( [0x80, 0xb0, 0x01, 123, 0x02, 0x00, (256-122)] )
if sw1 == 0x61:
	GET_RESPONSE = [0X00, 0XC0, 0x00, 0x00 ]
	apdu = GET_RESPONSE + [sw2]
	response, sw1, sw2 = cardservice.connection.transmit( apdu )
	result = ""
	for i in response:
		result = result+chr(i)
	f.write(result)
for d in range(0x02,0x15):
		response, sw1, sw2 = cardservice.connection.transmit( [0x80, 0xb0, d, 0x00, 0x02, 0x00, 0x80] )
		if sw1 == 0x61:
			GET_RESPONSE = [0X00, 0XC0, 0x00, 0x00 ]
			apdu = GET_RESPONSE + [sw2]
			response, sw1, sw2 = cardservice.connection.transmit( apdu )
			result = ""
			for i in response:
				result = result+chr(i)
			f.write(result)
		response, sw1, sw2 = cardservice.connection.transmit( [0x80, 0xb0, d, 0x80, 0x02, 0x00, 0x80] )
		if sw1 == 0x61:
			GET_RESPONSE = [0X00, 0XC0, 0x00, 0x00 ]
			apdu = GET_RESPONSE + [sw2]
			response, sw1, sw2 = cardservice.connection.transmit( apdu )
			result = ""
			for i in response:
				result = result+chr(i)
			f.write(result)
response, sw1, sw2 = cardservice.connection.transmit( [0x80, 0xb0, 0x15, 0x00, 0x02, 0x00, 0x79] )
if sw1 == 0x61:
	GET_RESPONSE = [0X00, 0XC0, 0x00, 0x00 ]
	apdu = GET_RESPONSE + [sw2]
	response, sw1, sw2 = cardservice.connection.transmit( apdu )
	result = ""
	for i in response:
		result = result+chr(i)
	f.write(result)
