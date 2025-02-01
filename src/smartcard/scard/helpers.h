/*==============================================================================
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
================================================================================
==============================================================================*/

typedef struct
{
    int bAllocated;
    unsigned char* ab;
    SCARDDWORDARG cBytes;
} BYTELIST ;

typedef char* ERRORSTRING;

#ifdef PCSCLITE
typedef struct
{
    unsigned long  Data1;
    unsigned short Data2;
    unsigned short Data3;
    unsigned char  Data4[ 8 ];
} GUID;
#endif

typedef struct
{
    int bAllocated;
    GUID* aguid;
    unsigned long cGuids;
    SCARDCONTEXT hcontext;
} GUIDLIST ;

typedef struct
{
    SCARD_READERSTATE* ars;
    char** aszReaderNames;
    int cRStates;
} READERSTATELIST ;

typedef struct
{
    int bAllocated;
    SCARDCONTEXT hcontext;
    char* sz;
} STRING;

typedef struct
{
    int bAllocated;
    SCARDCONTEXT hcontext;
    char* ac;
} STRINGLIST ;


/**=============================================================================
          F U N C T I O N   P R O T O T Y P E S
==============================================================================*/
// BYTELIST helpers
void SCardHelper_AppendByteListToPyObject( BYTELIST* source, PyObject** ptarget );
BYTELIST* SCardHelper_PyByteListToBYTELIST(PyObject* source);

// ERRORSTRING helpers
void SCardHelper_OutErrorStringAsPyObject( ERRORSTRING source, PyObject** ptarget );

// GUIDLIST helpers
void SCardHelper_AppendGuidListToPyObject( GUIDLIST* source, PyObject** ptarget );
GUIDLIST* SCardHelper_PyGuidListToGUIDLIST(PyObject* source);
void SCardHelper_PrintGuidList( GUIDLIST* apsz );

// READERSTATELIST helpers
void SCardHelper_AppendReaderStateListToPyObject( READERSTATELIST* source, PyObject** ptarget );
READERSTATELIST* SCardHelper_PyReaderStateListToREADERSTATELIST(PyObject* source);

// SCARDCONTEXT helpers
void SCardHelper_AppendSCardContextToPyObject( SCARDCONTEXT source, PyObject** ptarget );
SCARDCONTEXT SCardHelper_PyScardContextToSCARDCONTEXT( PyObject* source );

// SCARDHANDLE helpers
void SCardHelper_AppendSCardHandleToPyObject( SCARDHANDLE source, PyObject** ptarget );
SCARDHANDLE SCardHelper_PyScardHandleToSCARDHANDLE( PyObject* source );

// SCARDDWORDARG helpers
void SCardHelper_AppendSCardDwordArgToPyObject( SCARDDWORDARG source, PyObject** ptarget );
SCARDDWORDARG SCardHelper_PySCardDwordArgToSCARDDWORDARG( PyObject* source );

// STRING helpers
void SCardHelper_AppendStringToPyObject( STRING* source, PyObject** ptarget );
STRING* SCardHelper_PyStringToString( PyObject* source );
void SCardHelper_PrintString( STRING* str );

// STRINGLIST helpers
void SCardHelper_AppendStringListToPyObject( STRINGLIST* source, PyObject** ptarget );
STRINGLIST* SCardHelper_PyStringListToStringList(PyObject* source);
void SCardHelper_PrintStringList( STRINGLIST* apsz );
