/*===========================================================================
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
===========================================================================*/
#ifdef WIN32
    #include <windows.h>
#endif

#ifdef __APPLE__
#include <PCSC/winscard.h>
#else
#include <winscard.h>
#endif

#include <Python.h>
#include <assert.h>

#include "pcsctypes.h"
#include "helpers.h"
#include "memlog.h"

extern PyObject* PyExc_SCardError;

#ifdef PCSCLITE
    #define FALSE (0==1)
    #define TRUE (1==1)
    #define lstrlen strlen
#endif // PCSCLITE


/**=======================================================================**/
static int _IsAReaderState( PyObject* o)
/*===========================================================================
===========================================================================*/
{
    PyObject* o2;

    // expecting at least 2 items: reader name and current state
    if( (PyTuple_Size(o)!=2) && (PyTuple_Size(o)!=3) )
    {
        PyErr_SetString( PyExc_TypeError, "Expecting two or three items in tuple." );
        return 0;
    }

    o2 = PyTuple_GetItem(o, 0);
    if(!PyUnicode_Check(o2))
    {
        PyErr_SetString( PyExc_TypeError, "Expected a string as reader name." );
        return 0;
    }
    o2 = PyTuple_GetItem(o, 1);
    if(!PyLong_Check(o2))
    {
        PyErr_SetString( PyExc_TypeError, "Expected an Int as second tuple item." );
        return 0;
    }
    if(PyTuple_Size(o)==3)
    {
        o2 = PyTuple_GetItem(o, 2);
        if(!PyList_Check(o2))
        {
            PyErr_SetString( PyExc_TypeError, "Expected a list as third tuple item." );
            return 0;
        }
    }
    return 1;
}

/**=======================================================================**/
static int _ReaderStateFromTuple( PyObject* o, READERSTATELIST* prl, unsigned int x )
/*===========================================================================
===========================================================================*/
{
    char* psz;
    PyObject* o2;
    PyObject* temp_bytes;

    // first tuple item is reader name
    o2=PyTuple_GetItem(o, 0);

    // Convert the readername from string (unicode) to bytes (ascii)
    temp_bytes = PyUnicode_AsEncodedString(o2, "ASCII", "strict"); // Owned reference
    if (temp_bytes != NULL)
    {
        psz = PyBytes_AsString(temp_bytes); // Borrowed pointer
        if (NULL == psz)
            return 0;
    }
    else
        return 0;

    prl->aszReaderNames[x] = mem_Malloc(strlen(psz)+1);
    if (!prl->aszReaderNames[x])
    {
        PyErr_SetString( PyExc_MemoryError, "Unable to allocate temporary array" );
        return 0;
    }
    prl->ars[x].szReader = prl->aszReaderNames[x];
    strcpy( prl->aszReaderNames[x], psz );

    Py_DECREF(temp_bytes);

    // second tuple item is current state
    o2=PyTuple_GetItem(o, 1);
    prl->ars[x].dwCurrentState = (SCARDDWORDARG)PyLong_AsLong(o2);

    // third tuple item is the ATR (optionally)
    if(PyTuple_Size(o)==3)
    {
        BYTELIST* ATR = mem_Malloc(sizeof(BYTELIST));
        if( !ATR )
        {
            PyErr_SetString( PyExc_MemoryError, "Unable to allocate temporary array" );
            return 0;
        }
        o2 = PyTuple_GetItem(o, 2);

        ATR = SCardHelper_PyByteListToBYTELIST(o2);
        memcpy(prl->ars[x].rgbAtr, ATR->ab, ATR->cBytes);
        prl->ars[x].cbAtr = ATR->cBytes;
        mem_Free(ATR);
    }
    return 1;
}


/**==========================================================================
                            BYTELIST Helpers
===========================================================================*/

/**=======================================================================**/
void SCardHelper_AppendByteListToPyObject(
    BYTELIST* source, PyObject** ptarget )
/*===========================================================================
builds a Python list from a byte list
===========================================================================*/
{
    PyObject* oByteList;

    // create byte list...
    if( (NULL!=source) && (NULL!=source->ab) )
    {
        unsigned int i;
        oByteList = PyList_New( source->cBytes );
        for(i=0; i<source->cBytes; i++)
        {
            PyObject* pyby;
            pyby = Py_BuildValue( "b", source->ab[i] );
            PyList_SetItem( oByteList, i, pyby );
        }
    }
    else
    {
        oByteList = PyList_New( 0 );
    }

    // append list to target
    if( !*ptarget )
    {
        *ptarget = oByteList;
    }
    else if( *ptarget == Py_None )
    {
        Py_DECREF(Py_None);
        *ptarget = oByteList;
    }
    else
    {
        if( !PyList_Check(*ptarget) )
        {
            PyObject* o2 = *ptarget;
            *ptarget = PyList_New(0);
            PyList_Append(*ptarget,o2);
            Py_XDECREF(o2);
        }
        PyList_Append(*ptarget,oByteList);
        Py_XDECREF(oByteList);
    }

}


/**=======================================================================**/
BYTELIST* SCardHelper_PyByteListToBYTELIST(PyObject* source)
/*===========================================================================
build a Python byte list from a BYTELIST
===========================================================================*/
{
    Py_ssize_t cBytes, x;
    BYTELIST* pbl;


    // sanity check
    if (!PyList_Check(source))
    {
        PyErr_SetString( PyExc_TypeError, "Expected a list object." );
        return NULL;
    }

    cBytes = PyList_Size(source);
    for( x=0; x<cBytes; x++)
    {
        PyObject* o = PyList_GetItem( source, x );
        if( !PyLong_Check(o) )
        {
            PyErr_SetString( PyExc_TypeError, "Expected a list of bytes." );
            return NULL;
        }
    }


    pbl=mem_Malloc(sizeof(BYTELIST));
    if( !pbl )
    {
        PyErr_SetString( PyExc_MemoryError, "Unable to allocate temporary array" );
        return NULL;
    }

    if (cBytes>0)
    {
        pbl->ab = mem_Malloc( cBytes*sizeof(unsigned char) );
        if( !pbl->ab )
        {
            PyErr_SetString( PyExc_MemoryError, "Unable to allocate temporary array" );
            mem_Free( pbl );
            return NULL;
        }
    }
    else
    {
        pbl->ab=NULL;
    }
    pbl->bAllocated=TRUE;
    pbl->cBytes=(SCARDDWORDARG)cBytes;


    for( x=0; x<cBytes; x++ )
    {
        PyObject* o = PyList_GetItem(source, x);
        pbl->ab[x] = (unsigned char)PyLong_AsLong(o);
    }
    return (BYTELIST*)pbl;
}


/**==========================================================================
                            ERRORSTRING Helpers
===========================================================================*/

/**=======================================================================**/
void SCardHelper_OutErrorStringAsPyObject(
    ERRORSTRING source, PyObject** ptarget )
/*===========================================================================
Builds a Python string from an ERRORSTRING
===========================================================================*/
{
    PyObject* pystr;

    if( NULL!=source )
    {
#if defined(WIN32)
        pystr = PyUnicode_DecodeLocale(source, NULL);
#else
        pystr = PyUnicode_FromString( source );
#endif
        *ptarget = pystr;
    }
    else
    {
        *ptarget = Py_None;
        Py_INCREF(Py_None);
    }
}

/**==========================================================================
                            GUIDLIST Helpers
===========================================================================*/

/**=======================================================================**/
void SCardHelper_AppendGuidListToPyObject(
    GUIDLIST* source, PyObject** ptarget )
/*===========================================================================
build a Python GUID list from a C GUID list
===========================================================================*/
{
    PyObject* oByte;
    PyObject* oGuildItem;
    PyObject* oGuidList;
    unsigned char* pc;
    unsigned int i, j;

    // create GUID list...
    for(;;)
    {
        if (source!=NULL)
        {

            // create GUID list
            oGuidList = PyList_New( source->cGuids );
            if(NULL==oGuidList)
            {
                PyErr_SetString( PyExc_MemoryError, "Unable to allocate GUID list" );
                break;
            }
            for( i=0; i<source->cGuids; i++)
            {
                oGuildItem=PyList_New( sizeof(GUID) );
                if(NULL==oGuildItem)
                {
                    PyErr_SetString( PyExc_MemoryError, "Unable to allocate GUID item list" );
                    break;
                }
                pc=(unsigned char*)&source->aguid[i];

                for (j=0; j<sizeof(GUID); j++)
                {
                    oByte = Py_BuildValue( "b", pc[j] );
                    PyList_SetItem( oGuildItem, j, oByte );
                }
                PyList_SetItem( oGuidList, i, oGuildItem );
            }
        }
        else
        {
            oGuidList = PyList_New( 0 );
            if(NULL==oGuidList)
            {
                PyErr_SetString( PyExc_MemoryError, "Unable to allocate GUID list" );
                break;
            }
        }
        break;
    }

    // append list to target
    if( !*ptarget )
    {
        *ptarget = oGuidList;
    }
    else if( *ptarget == Py_None )
    {
        Py_DECREF(Py_None);
        *ptarget = oGuidList;
    }
    else
    {
        if( !PyList_Check(*ptarget) )
        {
            PyObject* o2 = *ptarget;
            *ptarget = PyList_New(0);
            PyList_Append(*ptarget,o2);
            Py_XDECREF(o2);
        }
        PyList_Append(*ptarget,oGuidList);
        Py_XDECREF(oGuidList);
    }

}

/**=======================================================================**/
GUIDLIST* SCardHelper_PyGuidListToGUIDLIST(PyObject* source)
/*===========================================================================
build a Python byte list from a GUIDLIST
===========================================================================*/
{
    Py_ssize_t cBytes, cGuids, x;
    //int iGuid, iByte;
    GUIDLIST* pgl;
    unsigned char* p;


    // sanity check

    // do we have a list?
    if (!PyList_Check(source))
    {
        PyErr_SetString( PyExc_TypeError, "Expected a list object." );
        return NULL;
    }

    // is the list size a multiple of sizeof(GUID)?
    cBytes = PyList_Size(source);
    cGuids = cBytes/sizeof(GUID);
    if( (size_t)cBytes!=sizeof(GUID)*cGuids )
    {
        PyErr_SetString( PyExc_TypeError, "Invalid GUID list size." );
        return NULL;
    }

    // is it a list of bytes?
    for( x=0; x<cBytes; x++)
    {
        PyObject* o = PyList_GetItem( source, x );
        if( !PyLong_Check(o) )
        {
            PyErr_SetString( PyExc_TypeError, "Expected a list of bytes." );
            return NULL;
        }
    }


    // now we can talk

    // allocate GUIDLIST
    pgl=mem_Malloc(sizeof(GUIDLIST));
    if( NULL==pgl )
    {
        PyErr_SetString( PyExc_MemoryError, "Unable to allocate temporary array" );
        return NULL;
    }
    pgl->bAllocated=TRUE;
    pgl->cGuids=(unsigned long)cGuids;
    pgl->hcontext=(unsigned long)NULL;

    // allocate GUIDs in GUID list
    if (cGuids>0)
    {
        pgl->aguid = mem_Malloc( cGuids*sizeof(GUID) );
        if( NULL==pgl->aguid )
        {
            PyErr_SetString( PyExc_MemoryError, "Unable to allocate temporary array" );
            mem_Free( pgl );
            return NULL;
        }
    }
    else
    {
        pgl->aguid=NULL;
    }


    // fill individual GUIDs
    /*
    for( iGuid=0; iGuidx<cGuids; iGuid++ )
    {
        p=(unsigned char*)pgl->aguid+iGuid*sizeof(GUID);
        for( x=0; x<sizeof(GUID); x++)
        {
            PyObject* o = PyList_GetItem(source, x);
            p[x] = (unsigned char)PyLong_AsLong(o);
        }
    }
    */

    p=(unsigned char*)pgl->aguid;
    for( x=0; x<cBytes; x++ )
    {
        PyObject* o = PyList_GetItem(source, x);
        p[x] = (unsigned char)PyLong_AsLong(o);
    }


    return (GUIDLIST*)pgl;
}

/**=======================================================================**/
void SCardHelper_PrintGuidList( GUIDLIST* apsz )
/*===========================================================================
dump a GUID list
===========================================================================*/
{
    unsigned long i, j;

    for(i=0; i<apsz->cGuids; i++)
    {
        unsigned char* pc=(unsigned char*)&apsz->aguid[i];
        for (j=0; j<sizeof(GUID); j++)
        {
            printf("0x%.2X ", pc[j] );
        }
        printf("\n");
    }
}


/**==========================================================================
                            READERSTATELIST Helpers
===========================================================================*/

/**=======================================================================**/
void SCardHelper_AppendReaderStateListToPyObject(
    READERSTATELIST* source, PyObject** ptarget )
/*===========================================================================
===========================================================================*/
{
    PyObject* oRStateList;
    //PyObject* o;
    int i;

    if(source!=NULL)
    {
        oRStateList = PyList_New( source->cRStates );
        for( i=0; i<source->cRStates; i++ )
        {
            PyObject* oReader;
            PyObject* oEventState;
            PyObject* oAtr;
            PyObject* oByte;
            SCARDDWORDARG j;

            // reader, event state, atr
            PyObject* ot = PyTuple_New( 3 );
            oReader = PyUnicode_FromString( source->ars[i].szReader );
            oEventState = PyLong_FromLong( (SCARDDWORDARG)source->ars[i].dwEventState );
            // ATR visibly not initialised
            if ( source->ars[i].cbAtr > SCARD_ATR_LENGTH)
                source->ars[i].cbAtr = 0;

            oAtr = PyList_New( source->ars[i].cbAtr );
            for(j=0; j<source->ars[i].cbAtr; j++)
            {
                oByte = PyLong_FromLong( source->ars[i].rgbAtr[j] );
                PyList_SetItem( oAtr, j, oByte );
            }

            PyTuple_SetItem( ot, 0, oReader );
            PyTuple_SetItem( ot, 1, oEventState );
            PyTuple_SetItem( ot, 2, oAtr );

            PyList_SetItem( oRStateList, i, ot );

        }
    }
    else
    {
        oRStateList = PyList_New( 0 );
    }

    if( !*ptarget )
    {
        *ptarget = oRStateList;
    }
    else if( *ptarget == Py_None )
    {
        Py_DECREF(Py_None);
        *ptarget = oRStateList;
    }
    else
    {

        if( !PyList_Check(*ptarget) )
        {
            PyObject* o2 = *ptarget;
            *ptarget = PyList_New(0);
            PyList_Append(*ptarget,o2);
            Py_XDECREF(o2);
        }
        PyList_Append(*ptarget,oRStateList);
        Py_XDECREF(oRStateList);
    }
}

/**=======================================================================**/
READERSTATELIST* SCardHelper_PyReaderStateListToREADERSTATELIST(PyObject* source)
/*===========================================================================
build a READERSTATELIST from a Python list of reader states
===========================================================================*/
{
    SCARDDWORDARG cRStates, x;
    READERSTATELIST* prl;


    // sanity check
    if (!PyList_Check(source))
    {
        PyErr_SetString( PyExc_TypeError, "Expected a list object." );
        return NULL;
    }

    cRStates = (SCARDDWORDARG)PyList_Size(source);
    for( x=0; x<cRStates; x++)
    {
        PyObject* o = PyList_GetItem( source, x );
        if( !PyTuple_Check(o) )
        {
            PyErr_SetString( PyExc_TypeError, "Expected a list of tuples." );
            return NULL;
        }

        if( !_IsAReaderState(o) )
        {
            return NULL;
        }

    }

    prl=mem_Malloc(sizeof(READERSTATELIST));
    if(!prl)
    {
        PyErr_SetString( PyExc_MemoryError, "Unable to allocate temporary array" );
        return NULL;
    }
    prl->cRStates = cRStates;

    prl->ars = mem_Malloc( cRStates*sizeof(SCARD_READERSTATE) );
    if (!prl->ars)
    {
        PyErr_SetString( PyExc_MemoryError, "Unable to allocate temporary array" );
        mem_Free( prl );
        return NULL;
    }
	/* zeroise SCARD_READERSTATE to work with remote desktop */
	memset(prl->ars, 0, cRStates*sizeof(SCARD_READERSTATE) );

    prl->aszReaderNames = mem_Malloc( cRStates*sizeof(char*) );
    if (!prl->aszReaderNames)
    {
        PyErr_SetString( PyExc_MemoryError, "Unable to allocate temporary array" );
        mem_Free( prl->ars );
        mem_Free( prl );
        return NULL;
    }

    for( x=0; x<cRStates; x++ )
    {
        PyObject* o = PyList_GetItem(source, x);

        int iRes = _ReaderStateFromTuple( o, prl, x );
        if(!iRes)
        {
            SCARDDWORDARG j;
            for(j=0; j<x; j++)
            {
                mem_Free( prl->aszReaderNames[x] );
            }
            mem_Free( prl->ars );
            mem_Free( prl );
            return NULL;
        }
    }
    return (READERSTATELIST*)prl;
}


/**==========================================================================
                            SCARDCONTEXT Helpers
===========================================================================*/

/**=======================================================================**/
void SCardHelper_AppendSCardContextToPyObject(
    SCARDCONTEXT source, PyObject** ptarget )
/*===========================================================================
builds a Python SCARDCONTEXT from a C SCARDCONTEXT
===========================================================================*/
{
    PyObject* oScardContext;

    // create SCARDCONTEXT
    #ifdef PCSCLITE
        oScardContext = PyLong_FromLong( (long)source );
    #else // !PCSCLITE
        oScardContext = PyLong_FromVoidPtr( (void*)source );
    #endif // PCSCLITE

    // append list to target
    if( !*ptarget )
    {
        *ptarget = oScardContext;
    }
    else if( *ptarget == Py_None )
    {
        Py_DECREF(Py_None);
        *ptarget = oScardContext;
    }
    else
    {
        if( !PyList_Check(*ptarget) )
        {
            PyObject* o2 = *ptarget;
            *ptarget = PyList_New(0);
            PyList_Append(*ptarget,o2);
            Py_XDECREF(o2);
        }
        PyList_Append(*ptarget,oScardContext);
        Py_XDECREF(oScardContext);
    }
}

/**=======================================================================**/
SCARDCONTEXT SCardHelper_PyScardContextToSCARDCONTEXT(PyObject* source)
/*===========================================================================
build a SCARDCONTEXT from a python SCARDCONTEXT
===========================================================================*/
{
    SCARDCONTEXT scRet=0;

    // sanity check
    // do we have a python long?
    if (!PyLong_Check(source))
    {
        PyErr_SetString( PyExc_TypeError, "Expected a python long as SCARDCONTEXT." );
        return 0;
    }

    #ifdef PCSCLITE
        scRet = PyLong_AsLong( source );
    #else // !PCSCLITE
        scRet = PyLong_AsVoidPtr( source );
    #endif // PCSCLITE

    return scRet;
}


/**==========================================================================
                            SCARDHANDLE Helpers
===========================================================================*/

/**=======================================================================**/
void SCardHelper_AppendSCardHandleToPyObject(
    SCARDHANDLE source, PyObject** ptarget )
/*===========================================================================
builds a Python SCARDHANDLE from a C SCARDHANDLE
===========================================================================*/
{
    PyObject* oScardHandle;

    // create SCARDHANDLE
    #ifdef PCSCLITE
        oScardHandle = PyLong_FromLong( (long)source );
    #else // !PCSCLITE
        oScardHandle = PyLong_FromVoidPtr( (void*)source );
    #endif // PCSCLITE

    // append list to target
    if( !*ptarget )
    {
        *ptarget = oScardHandle;
    }
    else if( *ptarget == Py_None )
    {
        Py_DECREF(Py_None);
        *ptarget = oScardHandle;
    }
    else
    {
        if( !PyList_Check(*ptarget) )
        {
            PyObject* o2 = *ptarget;
            *ptarget = PyList_New(0);
            PyList_Append(*ptarget,o2);
            Py_XDECREF(o2);
        }
        PyList_Append(*ptarget,oScardHandle);
        Py_XDECREF(oScardHandle);
    }
}

/**=======================================================================**/
SCARDCONTEXT SCardHelper_PyScardHandleToSCARDHANDLE(PyObject* source)
/*===========================================================================
build a SCARDHANDLE from a python SCARDHANDLE
===========================================================================*/
{
    SCARDHANDLE scRet=0;

    // sanity check
    // do we have a python long?
    if (!PyLong_Check(source))
    {
        PyErr_SetString( PyExc_TypeError, "Expected a python long as SCARDHANDLE." );
        return 0;
    }

    #ifdef PCSCLITE
        scRet = PyLong_AsLong( source );
    #else // !PCSCLITE
        scRet = PyLong_AsVoidPtr( source );
    #endif // PCSCLITE

    return scRet;
}

/**==========================================================================
                            SCARDDWORDARG Helpers
===========================================================================*/

/**=======================================================================**/
void SCardHelper_AppendSCardDwordArgToPyObject(
    SCARDDWORDARG source, PyObject** ptarget )
/*===========================================================================
builds a Python SCARDDWORDARG from a C SCARDDWORDARG
===========================================================================*/
{
    PyObject* oScardDword;

    // create SCARDDWORDARG
    #ifdef PCSCLITE
        oScardDword = PyLong_FromLong( (long)source );
    #else // !PCSCLITE
        oScardDword = PyLong_FromUnsignedLong( (unsigned long)source );
    #endif // PCSCLITE

    // append list to target
    if( !*ptarget )
    {
        *ptarget = oScardDword;
    }
    else if( *ptarget == Py_None )
    {
        Py_DECREF(Py_None);
        *ptarget = oScardDword;
    }
    else
    {
        if( !PyList_Check(*ptarget) )
        {
            PyObject* o2 = *ptarget;
            *ptarget = PyList_New(0);
            PyList_Append(*ptarget,o2);
            Py_XDECREF(o2);
        }
        PyList_Append(*ptarget,oScardDword);
        Py_XDECREF(oScardDword);
    }
}

/**=======================================================================**/
SCARDDWORDARG SCardHelper_PySCardDwordArgToSCARDDWORDARG(PyObject* source)
/*===========================================================================
build a SCARDDWORDARG from a python SCARDDWORDARG
===========================================================================*/
{
    SCARDDWORDARG scRet=0;

    // sanity check
    // do we have a python long or int?
    if( !PyLong_Check(source) )
    {
        PyErr_SetString( PyExc_TypeError, "Expected a python integer or long." );
        return -1;
    }

    #ifdef PCSCLITE
        scRet = PyLong_AsLong( source );
    #else // !PCSCLITE
        scRet = PyLong_AsUnsignedLong( source );
    #endif // PCSCLITE

    return scRet;
}


/**==========================================================================
                            STRING Helpers
===========================================================================*/

/**=======================================================================**/
void SCardHelper_AppendStringToPyObject(
    STRING* source, PyObject** ptarget )
/*===========================================================================
Builds a Python string from a STRING
===========================================================================*/
{
    PyObject* pystr;

    if(NULL!=source)
    {
        if(NULL!=source->sz)
        {
            pystr = PyUnicode_FromString( source->sz );
        }
        else
        {
            pystr = Py_None;
            Py_INCREF(Py_None);
        }
        if( !*ptarget )
        {
            *ptarget = pystr;
        }
        else if( *ptarget == Py_None )
        {
            Py_DECREF(Py_None);
            *ptarget = pystr;
        }
        else
        {

            if( !PyList_Check(*ptarget) )
            {
                PyObject* o2 = *ptarget;
                *ptarget = PyList_New(0);
                PyList_Append(*ptarget,o2);
                Py_XDECREF(o2);
            }
            PyList_Append( *ptarget, pystr );
            Py_XDECREF( pystr );
        }
    }
    else
    {
        if( !*ptarget )
        {
            *ptarget = Py_None;
            Py_INCREF(Py_None);
        }
    }
}

/**=======================================================================**/
STRING* SCardHelper_PyStringToString( PyObject* source )
/*===========================================================================
Build a STRING from a Python string; the string is allocated and
will have to be freed externally to the wrapper
===========================================================================*/
{
    size_t ulLength;
    STRING* pstr=NULL;

    for(;;)
    {
        // sanity check
        if( !PyUnicode_Check( source ) )
        {
            PyErr_SetString( PyExc_TypeError, "Expected a string." );
            break;
        }

        pstr=(STRING*)mem_Malloc( sizeof(STRING) );
        if(NULL==pstr)
        {
            PyErr_SetString( PyExc_MemoryError, "Unable to allocate STRING" );
            break;
        }

        ulLength=strlen( PyBytes_AsString(source)) + 1 ;
        pstr->sz=(char*)mem_Malloc( ulLength );
        if(NULL==pstr->sz)
        {
            PyErr_SetString( PyExc_MemoryError, "Unable to allocate STRING buffer" );
            break;
        }

        strcpy( pstr->sz, PyBytes_AsString( source ) );
        break;
    }

    return pstr;
}

/**=======================================================================**/
void SCardHelper_PrintString( STRING* str )
/*===========================================================================
dump a string list
===========================================================================*/
{
    if(NULL!=str)
    {
        char* p=str->sz;
        if( NULL!=p)
        {
            printf("%s ", p );
        }
    }
}

/**==========================================================================
                            STRINGLIST Helpers
===========================================================================*/


/**=======================================================================**/
void SCardHelper_AppendStringListToPyObject(
    STRINGLIST* source, PyObject** ptarget )
/*===========================================================================
builds a Python list from a STRINGLIST; the multi-string list in the STRINGLIST
is stored as series of null-terminated strings terminated by a null,
e.g. item0\0item2\0lastitem\0\0)
===========================================================================*/
{
    unsigned int cStr;
    char* p=source->ac;
    PyObject* oStrList;
    //PyObject* o;

    // count STRs in STRINGLIST list
    if( NULL!=p )
    {
        unsigned int i;
        for( i=0, cStr=0; ; i+=lstrlen( p+i ) + 1 )
        {
            if (lstrlen( p+i ) > 0)
            {
                cStr++;
            }
            else
            {
                break;
            }
        }
    }
    else
    {
        cStr=0;
    }

    // create STR list...
    if( NULL!=p )
    {
        unsigned int i, j;
        oStrList = PyList_New( cStr );
        for( i=0, j=0; ; j++, i+=lstrlen( p+i ) + 1 )
        {
            if (lstrlen( p+i ) > 0)
            {
                PyObject* pystr;
                pystr = PyUnicode_FromString( p+i );
                PyList_SetItem( oStrList, j, pystr );
            }
            else
            {
                break;
            }
        }
    }
    else
    {
        oStrList = PyList_New( cStr );
    }

    if( !*ptarget )
    {
        *ptarget = oStrList;
    }
    else if( *ptarget == Py_None )
    {
        Py_DECREF(Py_None);
        *ptarget = oStrList;
    }
    else
    {

        if( !PyList_Check(*ptarget) )
        {
            PyObject* o2 = *ptarget;
            *ptarget = PyList_New(0);
            PyList_Append(*ptarget,o2);
            Py_XDECREF(o2);
        }
        PyList_Append(*ptarget,oStrList);
        Py_XDECREF(oStrList);
    }

}

/**=======================================================================**/
STRINGLIST* SCardHelper_PyStringListToStringList(PyObject* source)
/*===========================================================================
build a Python string list from a STRINGLIST
===========================================================================*/
{
    Py_ssize_t cStrings, cChars, x;
    STRINGLIST* psl;
    char* p;


    // sanity check
    if (!PyList_Check(source))
    {
        PyErr_SetString( PyExc_TypeError, "Expected a list object." );
        return NULL;
    }

    cStrings = PyList_Size(source);
    for( x=0, cChars=0; x<cStrings; x++)
    {
        PyObject* o = PyList_GetItem( source, x );
        if( !PyUnicode_Check(o) )
        {
            PyErr_SetString( PyExc_TypeError, "Expected a list of strings." );
            return NULL;
        }
        cChars += PyUnicode_GET_LENGTH(o) + 1 ;
    }
    cChars += 1;

    psl=mem_Malloc(sizeof(STRINGLIST));
    if(!psl)
    {
        PyErr_SetString( PyExc_MemoryError, "Unable to allocate temporary array" );
        return NULL;
    }
    psl->bAllocated=TRUE;
    psl->hcontext = 0;

    if ( cChars>1 )
    {
        psl->ac = mem_Malloc( cChars*sizeof(char) );
        if (!psl->ac)
        {
            PyErr_SetString( PyExc_MemoryError, "Unable to allocate temporary array" );
            mem_Free( psl );
            return NULL;
        }

        for( x=0, p=psl->ac; x<cStrings; x++ )
        {
            PyObject* o = PyList_GetItem(source, x);
            // Convert the group name from string (unicode) to bytes (ascii)
            PyObject * temp_bytes = PyUnicode_AsEncodedString(o, "ASCII", "strict"); // Owned reference
            if (temp_bytes != NULL)
            {
                char * psz = PyBytes_AsString(temp_bytes); // Borrowed pointer
                if (NULL == psz)
                    return 0;
                strcpy(p, psz);
                Py_DECREF(temp_bytes);
            }
            p += strlen( p ) + 1;
        }
        strcpy( p, "\0" );
    }
    else
    {
        psl->ac=NULL;
    }
    return (STRINGLIST*)psl;
}


/**=======================================================================**/
void SCardHelper_PrintStringList( STRINGLIST* sl )
/*===========================================================================
dump a string list
===========================================================================*/
{
    char* p=(char*)sl->ac;
    unsigned int i;

    for( i=0; ; i+=lstrlen( p+i ) + 1 )
    {
        if (lstrlen( p+i ) > 0)
        {
            printf("%s ", p+i );
        }
        else
        {
            printf("\n" );
            break;
        }
    }
}

#ifdef WIN32
/**=======================================================================**/
BOOL WINAPI DllMain( HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved )
/*===========================================================================
Initialize and clean-up memory logging on process attach and detach
===========================================================================*/
{
    switch(fdwReason)
    {
        case DLL_PROCESS_ATTACH:
            if (!mem_Init())
            {
                fprintf( stderr, "Failed to initialize memory logging services!\n" );
            }
            break;

        case DLL_THREAD_ATTACH:
            break;

        case DLL_THREAD_DETACH:
            break;

        case DLL_PROCESS_DETACH:
            if (!mem_CleanUp())
            {
                fprintf( stderr, "Failed to cleanup memory logging services!\n" );
            }
            break;
    }
    return TRUE;

    return 1;
}
#endif // WIN32
