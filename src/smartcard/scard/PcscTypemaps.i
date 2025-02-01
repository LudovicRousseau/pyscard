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
==============================================================================*/

// Tell SWIG to wrap all the wrappers with Python's thread macros
%exception
{
    Py_BEGIN_ALLOW_THREADS;
    $function
    Py_END_ALLOW_THREADS;
}


/*==============================================================================
//
// support for list of BYTEs, aka BYTELIST
//
==============================================================================*/

#ifdef SWIG(python)
#endif
%typemap(in,numinputs=0) BYTELIST *OUTPUT(BYTELIST temp)
{
    $1 = &temp;
    $1->ab = NULL;
    $1->bAllocated=FALSE;
}


// builds a byte list from a Python list
%typemap(in) BYTELIST* INPUT(BYTELIST*)
{
    $1 =  SCardHelper_PyByteListToBYTELIST( $input );
    if (NULL == $1)
        goto fail;
}

// release bytelist arg
%typemap(freearg) BYTELIST*
{
    if(NULL!=$1)
    {
        if(NULL!=$1->ab)
        {
            mem_Free( $1->ab );
        }
        if($1->bAllocated==TRUE)
        {
            mem_Free( $1 );
        }
    }
}

// builds a Python list from a byte list
%typemap(argout) BYTELIST *OUTPUT
{
    SCardHelper_AppendByteListToPyObject( $1, &$result );
}

// other names for BYTELIST as INPUT parameter
%apply BYTELIST* INPUT { BYTELIST* ATR };
%apply BYTELIST* INPUT { BYTELIST* ATTRIBUTESIN };
%apply BYTELIST* INPUT { BYTELIST* MASK };
%apply BYTELIST* INPUT { BYTELIST* APDUCOMMAND };
%apply BYTELIST* INPUT { BYTELIST* INBUFFER };

// other names for BYTELIST as OUTPUT parameter
%apply BYTELIST* OUTPUT { BYTELIST* ATROUT };
%apply BYTELIST* OUTPUT { BYTELIST* ATTRIBUTES };
%apply BYTELIST* OUTPUT { BYTELIST* APDURESPONSE };
%apply BYTELIST* OUTPUT { BYTELIST* OUTBUFFER };

/*==============================================================================
//
// support for ERRORSTRING
//
==============================================================================*/
%typemap(ret) ERRORSTRING
{
    #ifdef WIN32
    if(NULL!=$1)
    {
        HLOCAL hlocal = LocalFree( $1 );
        if(NULL!=hlocal)
        {
            fprintf( stderr, "Failed to free error message string!\n" );
        }
    }
    #endif // WIN32
    #ifdef PCSCLITE
        free( $1 );
    #endif // PCSCLITE
}

// builds a Python string from a STRING
%typemap(out) ERRORSTRING
{
    SCardHelper_OutErrorStringAsPyObject( $1, &$result );
}


/*==============================================================================
//
// support for GUIDLIST
//
==============================================================================*/


%typemap(in,numinputs=0) GUIDLIST *OUTPUT(GUIDLIST temp)
{
    $1 = &temp;
    $1->bAllocated=FALSE;
}

// release GUIDLIST INPUT argument
// for input arg, GUIDLIST was allocated from the heap
// i.e. $1 has to be freed
%typemap(freearg) GUIDLIST* INPUT
{
    if(NULL!=$1)
    {
        if(NULL!=$1->aguid)
        {
            if($1->hcontext)
            {
                unsigned long lRes=(mySCardFreeMemory)( $1->hcontext, $1->aguid );
                if (lRes!=SCARD_S_SUCCESS)
                {
                    fprintf( stderr, "kaboom!\n" );
                }
            }
            else
            {
                mem_Free( $1->aguid );
            }
        }
        mem_Free( $1 );
    }
}

// release GUIDLIST OUTPUT argument
// for output arg, GUIDLIST was not allocated
// from the heap, but from the stack
// i.e. $1 must not be freed
%typemap(freearg) GUIDLIST* OUTPUT
{
    if(NULL!=$1)
    {
        if(NULL!=$1->aguid)
        {
            if($1->hcontext)
            {
                unsigned long lRes=(mySCardFreeMemory)( $1->hcontext, $1->aguid );
                if (lRes!=SCARD_S_SUCCESS)
                {
                    fprintf( stderr, "kaboom!\n" );
                }
            }
            else
            {
                mem_Free( $1->aguid );
            }
        }
    }
}

// builds a win32 string list from a Python list
%typemap(in) GUIDLIST* INPUT(GUIDLIST*)
{
    $1 =  SCardHelper_PyGuidListToGUIDLIST( $input );
    if (NULL == $1)
        goto fail;
}

// builds a Python list from a GUID list
%typemap(argout) GUIDLIST *OUTPUT
{
    SCardHelper_AppendGuidListToPyObject( $1, &$result );
}

// other names for GUIDLIST as INPUT parameter
%apply GUIDLIST* INPUT { GUIDLIST* PRIMARYPROVIDER };
%apply GUIDLIST* INPUT { GUIDLIST* PROVIDERLIST };

// other names for GUIDLIST as OUTPUT parameter
%apply GUIDLIST* OUTPUT { GUIDLIST* GUIDINTERFACES };


/*==============================================================================
//
// support for READERSTATELIST*
//
==============================================================================*/


%typemap(in,numinputs=0) READERSTATELIST *OUTPUT(READERSTATELIST temp)
{
    $1 = &temp;
}

// release READERSTATELIST INPUT/OUTPUT argument
// for input arg, READERSTATELIST was allocated from the heap
// i.e. $1 has to be freed
%typemap(freearg) READERSTATELIST* BOTH
{
    if(NULL!=$1)
    {
        int i;
        for(i=0; i<$1->cRStates; i++ )
        {
            if($1->aszReaderNames[i])
            {
                mem_Free( $1->aszReaderNames[i] );
            }
        }
        if(NULL!=$1->ars)
        {
            mem_Free( $1->ars );
        }
        if(NULL!=$1->aszReaderNames)
        {
            mem_Free( $1->aszReaderNames );

        }
        mem_Free( $1 );
    }
}

// release READERSTATELIST OUTPUT argument
// for output arg, READERSTATELIST was not allocated
// from the heap, but from the stack
// i.e. $1 must not be freed
%typemap(freearg) READERSTATELIST* OUTPUT
{
    if(NULL!=$1)
    {
        int i;
        for(i=0; i<$1->cRStates; i++ )
        {
            if($1->aszReaderNames[i])
            {
                mem_Free( $1->aszReaderNames[i] );
            }
        }
        if(NULL!=$1->ars)
        {
            mem_Free( $1->ars );
        }
        if(NULL!=$1->aszReaderNames)
        {
            mem_Free( $1->aszReaderNames );

        }
    }
}

// builds a READERSTATE list string list from a Python list
%typemap(in) READERSTATELIST *prsl(READERSTATELIST*)
{
    $1 =  SCardHelper_PyReaderStateListToREADERSTATELIST( $input );
    if (NULL == $1)
        goto fail;
}

// builds a Python list from a win32 string list
%typemap(argout) READERSTATELIST *prsl
{
    SCardHelper_AppendReaderStateListToPyObject( $1, &$result );
}

// reader state list as input and output
//%typemap(in) READERSTATELIST *BOTH = READERSTATELIST *prsl;
//%typemap(argout) READERSTATELIST *BOTH = READERSTATELIST *prsl;


// other names for READERSTATELIST as input/output parameter
%apply READERSTATELIST *BOTH {READERSTATELIST* prsl};


/*==============================================================================
//
// support for SCARDCONTEXT
//
==============================================================================*/
%typemap(in,numinputs=0) SCARDCONTEXT *OUTPUT(SCARDCONTEXT temp)
{
    $1 = &temp;
}

%typemap(in) SCARDCONTEXT hcontext(SCARDCONTEXT)
{
    $1 =  SCardHelper_PyScardContextToSCARDCONTEXT( $input );
    if (0 == $1)
        goto fail;
}

%typemap(argout) SCARDCONTEXT *OUTPUT
{
    SCardHelper_AppendSCardContextToPyObject( *$1, &$result );
}

// different names for SCARDCONTEXT OUTPUT parameters
%apply SCARDCONTEXT* OUTPUT { SCARDCONTEXT* phcontext };


/*==============================================================================
//
// support for SCARDDWORDARG
//
==============================================================================*/
%typemap(in,numinputs=0) SCARDDWORDARG *OUTPUT(SCARDDWORDARG temp)
{
    $1 = &temp;
}

%typemap(in) SCARDDWORDARG INPUT(SCARDDWORDARG)
{
    $1 =  SCardHelper_PySCardDwordArgToSCARDDWORDARG( $input );
    if ((SCARDDWORDARG)-1 == $1)
        goto fail;
}

%typemap(argout) SCARDDWORDARG* OUTPUT
{
    SCardHelper_AppendSCardDwordArgToPyObject( *$1, &$result );
}

// different names for SCARDWORDARG INPUT parameters
%apply SCARDDWORDARG INPUT { SCARDDWORDARG dwProviderId };
%apply SCARDDWORDARG INPUT { SCARDDWORDARG dwShareMode };
%apply SCARDDWORDARG INPUT { SCARDDWORDARG dwPreferredProtocols };
%apply SCARDDWORDARG INPUT { SCARDDWORDARG dwDisposition };
%apply SCARDDWORDARG INPUT { SCARDDWORDARG dwScope };
%apply SCARDDWORDARG INPUT { SCARDDWORDARG dwAttrId };
%apply SCARDDWORDARG INPUT { SCARDDWORDARG dwTimeout };
%apply SCARDDWORDARG INPUT { SCARDDWORDARG dwInitialization };
%apply SCARDDWORDARG INPUT { SCARDDWORDARG dwControlCode };

// different names for SCARDWORDARG OUTPUT parameters
%apply SCARDDWORDARG* OUTPUT { SCARDDWORDARG* pdwActiveProtocol };
%apply SCARDDWORDARG* OUTPUT { SCARDDWORDARG* pdwProtocol };
%apply SCARDDWORDARG* OUTPUT { SCARDDWORDARG* pdwState };

/*==============================================================================
//
// support for SCARDHANDLE
//
==============================================================================*/
%typemap(in,numinputs=0) SCARDHANDLE *OUTPUT(SCARDHANDLE temp)
{
    $1 = &temp;
}

%typemap(in) SCARDHANDLE hcard(SCARDHANDLE)
{
    $1 =  SCardHelper_PyScardHandleToSCARDHANDLE( $input );
    if (0 == $1)
        goto fail;
}

%typemap(argout) SCARDHANDLE* OUTPUT
{
    SCardHelper_AppendSCardHandleToPyObject( *$1, &$result );
}

// different names for SCARDHANDLE OUTPUT parameters
%apply SCARDHANDLE* OUTPUT { SCARDHANDLE* phcard };


/*==============================================================================
//
// support for SCARDRETCODE
//
==============================================================================*/
%typemap(out) SCARDRETCODE
{
    $result = PyLong_FromLong((long)$1);
}

/*==============================================================================
//
// support for STRING
//
==============================================================================*/

// release STRING INPUT argument.
// string is allocated in SCardHelper_PyStringToString
// string->sz is always allocated
%typemap(freearg) STRING* INPUT
{
    if(NULL!=$1)
    {
        if(NULL!=$1->sz)
        {
            if($1->hcontext)
            {
                unsigned long lRes=(mySCardFreeMemory)( $1->hcontext, $1->sz );
                if (lRes!=SCARD_S_SUCCESS)
                {
                    fprintf( stderr, "kaboom!\n" );
                }
            }
            else
            {
                mem_Free( $1->sz );
            }
            $1->sz=NULL;
        }
        mem_Free( $1 );
    }
}

// release STRING OUTPUT argument.
// string is not allocated
// string->sz is always allocated
%typemap(freearg) STRING* OUTPUT
{
    if(NULL!=$1)
    {
        if(NULL!=$1->sz)
        {
            if($1->hcontext)
            {
                unsigned long lRes=(mySCardFreeMemory)( $1->hcontext, $1->sz );
                if (lRes!=SCARD_S_SUCCESS)
                {
                    fprintf( stderr, "kaboom!\n" );
                }
            }
            else
            {
                mem_Free( $1->sz );
            }
            $1->sz=NULL;
        }
    }
}

// force the argument to be ignored
%typemap(in,numinputs=0) STRING *OUTPUT(STRING temp)
{
    $1 = &temp;
    $1->bAllocated=FALSE;
}

// builds a string from a Python string
%typemap(in) STRING *INPUT( STRING )
{
    $1 =  SCardHelper_PyStringToString( $input );
    if (NULL == $1)
        goto fail;
}

// builds a Python string from a STRING
%typemap(argout) STRING *OUTPUT
{
    SCardHelper_AppendStringToPyObject( $1, &$result );
}

// other names for STRING as output parameter
%apply STRING* OUTPUT { PROVIDERNAME_t* pszProviderName };
%apply STRING* OUTPUT { STRING* pszReaderNameOut };

/*==============================================================================
//
// support for STRINGLIST
// SCardxxx API stores multi-strings as a concatenation
// of strings terminated by a null, e.g.
// item0\0item2\0lastitem\0\0
//
==============================================================================*/


// for OUTPUT STRINGLIST, free the allocated buffer
// for winscard, the buffer is automatically allocated and
// has to be freed by SCardFreeMemory.
// for pcsclite, the buffer is allocated with mem_Malloc and
// has to be freed by mem_Free.
%typemap(freearg) STRINGLIST*
{
    if(NULL!=$1)
    {
        if(NULL!=$1->ac)
        {
            if($1->hcontext)
            {
                unsigned long lRes=(mySCardFreeMemory)( $1->hcontext, $1->ac );
                if (lRes!=SCARD_S_SUCCESS)
                {
                    fprintf( stderr, "Failed to SCardFreeMemory!\n" );
                }
            }
            else
            {
                if( NULL!=$1->ac )
                {
                    mem_Free( $1->ac );
                }
            }
        }
        if($1->bAllocated==TRUE)
        {
            mem_Free( $1 );
        }
    }
}

%typemap(in,numinputs=0) STRINGLIST *OUTPUT(STRINGLIST temp)
{
    $1 = &temp;
    $1->bAllocated=FALSE;
}

// builds a win32 string list from a Python list
%typemap(in) STRINGLIST* INPUT(STRINGLIST*)
{
    $1 =  SCardHelper_PyStringListToStringList( $input );
    if (NULL == $1)
        goto fail;
}

// builds a Python list from a win32 string list
%typemap(argout) STRINGLIST *OUTPUT
{
    SCardHelper_AppendStringListToPyObject( $1, &$result );
}

// other names for STRINGLIST as input parameter
%apply STRINGLIST* INPUT { STRINGLIST* CARDSTOLOCATE };
%apply STRINGLIST* INPUT { STRINGLIST* psl };
%apply STRINGLIST* INPUT { STRINGLIST* READERGROUPSIN };

// other names for STRINGLIST as output parameter
%apply STRINGLIST* OUTPUT { STRINGLIST* MATCHINGCARDS };
%apply STRINGLIST* OUTPUT { STRINGLIST* READERSFOUND };
%apply STRINGLIST* OUTPUT { STRINGLIST* READERGROUPSOUT };
%apply STRINGLIST* OUTPUT { STRINGLIST* pszReaderName };


//#endif
