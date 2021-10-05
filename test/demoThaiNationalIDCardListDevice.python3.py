#  install pcscd python-pyscard python-pil
import os, io, binascii,sys, codecs
from PIL import Image
from smartcard.System import readers
from smartcard.util import HexListToBinString, toHexString, toBytes
# Thailand ID Smartcard
def thai2unicode(data):
 result = ''
 result = bytes(data).decode('tis-620')
 return result.strip();
def getData(cmd, req = [0x00, 0xc0, 0x00, 0x00]):
 data, sw1, sw2 = connection.transmit(cmd)
 data, sw1, sw2 = connection.transmit(req + [cmd[-1]])
 return [data, sw1, sw2];
# Check card
SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08]
THAI_CARD = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]
# CID
CMD_CID = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]
# TH Fullname
CMD_THFULLNAME = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0x64]
# EN Fullname
CMD_ENFULLNAME = [0x80, 0xb0, 0x00, 0x75, 0x02, 0x00, 0x64]
# Date of birth
CMD_BIRTH = [0x80, 0xb0, 0x00, 0xD9, 0x02, 0x00, 0x08]
# Gender
CMD_GENDER = [0x80, 0xb0, 0x00, 0xE1, 0x02, 0x00, 0x01]
# Card Issuer
CMD_ISSUER = [0x80, 0xb0, 0x00, 0xF6, 0x02, 0x00, 0x64]
# Issue Date
CMD_ISSUE = [0x80, 0xb0, 0x01, 0x67, 0x02, 0x00, 0x08]
# Expire Date
CMD_EXPIRE = [0x80, 0xb0, 0x01, 0x6F, 0x02, 0x00, 0x08]
# Address
CMD_ADDRESS = [0x80, 0xb0, 0x15, 0x79, 0x02, 0x00, 0x64]
# Photo_Part1/20
CMD_PHOTO1 = [0x80, 0xb0, 0x01, 0x7B, 0x02, 0x00, 0xFF]
# Get all the available readers
readerList = readers()
print ('Available readers:')
for readerIndex,readerItem in enumerate(readerList):
 print(readerIndex, readerItem)
# Select reader
readerSelectIndex = 0 #int(input("Select reader[0]: ") or "0")
reader = readerList[readerSelectIndex]
print ("Using:", reader)
connection = reader.createConnection()
connection.connect()
atr = connection.getATR()
print ("ATR: " + toHexString(atr))
if (atr[0] == 0x3B & atr[1] == 0x67):
 req = [0x00, 0xc0, 0x00, 0x01]
else :
 req = [0x00, 0xc0, 0x00, 0x00]
# Check card
data, sw1, sw2 = connection.transmit(SELECT + THAI_CARD)
print ("Select Applet: %02X %02X" % (sw1, sw2))
# CID
data = getData(CMD_CID, req)
cid = thai2unicode(data[0])
print ("CID: " + cid)
# TH Fullname
data = getData(CMD_THFULLNAME, req)
print ("TH Fullname: " +  thai2unicode(data[0]))
#print(thai2unicode2(data[0])))
# EN Fullname
data = getData(CMD_ENFULLNAME, req)
print ("EN Fullname: " + thai2unicode(data[0]))
# Date of birth
data = getData(CMD_BIRTH, req)
print( "Date of birth: " + thai2unicode(data[0]))
# Gender
data = getData(CMD_GENDER, req)
print ("Gender: " + thai2unicode(data[0]))
# Card Issuer
data = getData(CMD_ISSUER, req)
print ("Card Issuer: " + thai2unicode(data[0]))
# Issue Date
data = getData(CMD_ISSUE, req)
print ("Issue Date: " + thai2unicode(data[0]))
# Expire Date
data = getData(CMD_EXPIRE, req)
print ("Expire Date: " + thai2unicode(data[0]))
# Address
data = getData(CMD_ADDRESS, req)
print ("Address: " + thai2unicode(data[0]))
# Exit program
sys.exit()
