/*==============================================================================
Copyright 2001-2012 gemalto
Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
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
==============================================================================*/

%define DOCSTRING
"The smartcard.scard module is a simple wrapper on top of the C language
PCSC SCardXXX API.

The smartcard.scard module is the lower layer of the pyscard
framework that provides a higher level interface.

You should avoid using the L{smartcard.scard} package directly, and use the
pyscard directly because:

 - smartcard.scard being a C wrapper, the code tends to look like C code
   written in python syntax

 - the smartcard package provides higher level abstractions (e.g.
   L{CardType}, L{CardConnection}), and makes programming easier since it is
   totally written in Python

You can still use the smartcard.scard package if you want to write your
own framework, or if you want to perform quick-and-dirty port of C
language programs using SCardXXX calls, or if there are features of
SCardXXX API that you want to use and that are not available in the
pyscard library.

Introduction

The smartcard.scard module is a Python wrapper around PCSC smart card base
services.  On Windows, the wrapper is performed around the smart card base
components winscard library.  On linux and OS X, the wrapper is performed
around the PCSC-lite library.


The smartcard.scard module provides mapping for the following API functions,
depending on the Operating System::

    =============================== ======= =======
    Function                        Windows  Linux
                                             OS X
    =============================== ======= =======
    GetOpenCardName
    SCardAddReaderToGroup              Y
    SCardBeginTransaction              Y       Y
    SCardCancel                        Y       Y
    SCardConnect                       Y       Y
    SCardControl                       Y       Y
    SCardDisconnect                    Y       Y
    SCardEndTransaction                Y       Y
    SCardEstablishContext              Y       Y
    SCardForgetCardType                Y
    SCardForgetReader                  Y
    SCardForgetReaderGroup             Y
    SCardFreeMemory
    SCardGetAttrib                     Y       Y
    SCardGetCardTypeProviderName       Y
    SCardGetErrorMessage               Y       Y
    SCardGetProviderId
    SCardGetStatusChange               Y       Y
    SCardIntroduceCardType             Y
    SCardIntroduceReader               Y
    SCardIntroduceReaderGroup          Y
    SCardIsValidContext                Y       Y
    SCardListCards                     Y
    SCardListInterfaces                Y
    SCardListReaderGroups              Y       Y
    SCardListReaders                   Y       Y
    SCardLocateCards                   Y
    SCardReconnect                     Y       Y
    SCardReleaseContext                Y       Y
    SCardRemoveReaderFromGroup         Y
    SCardSetAttrib                     Y       Y
    SCardSetCartTypeProviderName
    SCardStatus                        Y       Y
    SCardTransmit                      Y       Y
    SCardUIDlgSelectCard
    =============================== ======= =======

Comments, bug reports, improvements welcome.

-------------------------------------------------------------------------------

Copyright 2001-2012 gemalto
@Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
@Author: Ludovic Rousseau, mailto:ludovic.rousseau@free.fr

This file is part of pyscard.

pyscard is free software; you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 2.1 of the License, or (at
your option) any later version.

pyscard is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyscard; if not, write to the Free Software Foundation,
Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
"
%enddef

%module(docstring=DOCSTRING, package="smartcard.scard") scard

%feature("autodoc", "1");

%{
#ifdef WIN32
#include <windows.h>
#endif

#ifdef __APPLE__
#include <PCSC/winscard.h>
#else
#include <winscard.h>
#endif

#ifdef PCSCLITE
    #ifdef __APPLE__
        #include "pyscard-reader.h"
        #ifndef SCARD_CTL_CODE
            #define SCARD_CTL_CODE(code) (0x42000000 + (code))
        #endif
    #else
        #include <reader.h>
    #endif
    // undefined on older releases
    #ifndef MAX_BUFFER_SIZE_EXTENDED
        #define MAX_BUFFER_SIZE_EXTENDED    (4 + 3 + (1<<16) + 3 + 2)
    #endif
#else // !PCSCLITE
// SCARD_CTL_CODE defined in WinSmCrd.h included by Win32 winscard.h
// MAX_BUFFER_SIZE_EXTENDED is pcsc-lite specific
// Issues on Lenovo laptop with NXP reader for higher values
// See https://github.com/LudovicRousseau/pyscard/issues/100
#define MAX_BUFFER_SIZE_EXTENDED   65535
#endif //PCSCLITE

#include "pcsctypes.h"
#include "helpers.h"
#include "memlog.h"

#include "winscarddll.h"

typedef STRING PROVIDERNAME_t;

%}

%include typemaps.i
%include PcscTypemaps.i

%{

//
// these functions are only available on win32 PCSC
//

#ifdef WIN32
///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _AddReaderToGroup(
  SCARDCONTEXT hcontext,
  char* szReaderName,
  char* szGroupName)
{
    return (mySCardAddReaderToGroupA)(
                         hcontext,
                         szReaderName,
                         szGroupName);
}

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _ForgetCardType(SCARDCONTEXT hcontext, char* pszCardName)
{
    return (mySCardForgetCardTypeA)(hcontext, pszCardName);
}

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _ForgetReader(SCARDCONTEXT hcontext, char* szReaderName)
{
    return (mySCardForgetReaderA)(hcontext, szReaderName);
}

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _ForgetReaderGroup(SCARDCONTEXT hcontext, char* szGroupName)
{
    return (mySCardForgetReaderGroupA)(hcontext, szGroupName);
}

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _GetCardTypeProviderName(
    SCARDCONTEXT hcontext,
    char* pszCardName,
    SCARDDWORDARG dwProviderId,
    PROVIDERNAME_t* psl)
{
    long lRetCode;
    unsigned long cchProviderName=SCARD_AUTOALLOCATE;


    // autoallocate memory; will be freed on output typemap
    psl->hcontext=hcontext;
    psl->sz=NULL;

    lRetCode=(mySCardGetCardTypeProviderNameA)(
        hcontext, pszCardName, dwProviderId,
        (LPTSTR)&psl->sz, &cchProviderName);

    return lRetCode;
};

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _IntroduceCardType(
  SCARDCONTEXT hcontext,
  char* pszCardName,
  GUIDLIST* pguidPrimaryProvider,
  GUIDLIST* rgguidInterfaces,
  BYTELIST* pbAtr,
  BYTELIST* pbAtrMask
)
{
    return (mySCardIntroduceCardTypeA)(
                hcontext,
                pszCardName,
                pguidPrimaryProvider ? pguidPrimaryProvider->aguid : NULL,
                rgguidInterfaces ? rgguidInterfaces->aguid : NULL,
                rgguidInterfaces ? rgguidInterfaces->cGuids : 0,
                pbAtr->ab,
                pbAtrMask->ab,
                pbAtr->cBytes);
}

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _IntroduceReader(SCARDCONTEXT hcontext, char* szReaderName, char* szDeviceName)
{
    return (mySCardIntroduceReaderA)(hcontext, szReaderName, szDeviceName);
}

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _IntroduceReaderGroup(SCARDCONTEXT hcontext, char* szGroupName)
{
    return (mySCardIntroduceReaderGroupA)(hcontext, szGroupName);
}

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _ListCards(SCARDCONTEXT hcontext, BYTELIST* pbl, GUIDLIST* guidlist, STRINGLIST* pmszCards)
{
    // autoallocate memory; will be freed on output typemap
    unsigned long cchCards=SCARD_AUTOALLOCATE;

    pmszCards->ac=NULL;
    pmszCards->hcontext=hcontext;

    return (mySCardListCardsA)(
        hcontext,
        pbl->ab,
        (NULL==guidlist) ? NULL : guidlist->aguid,
        (NULL==guidlist) ? 0 : guidlist->cGuids,
        (LPTSTR)&pmszCards->ac,
        &cchCards);
};


///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _ListInterfaces(
    SCARDCONTEXT hcontext,
    char* pszCard,
    GUIDLIST* pgl
)
{
    long lRetCode;

    pgl->cGuids = SCARD_AUTOALLOCATE;
    pgl->hcontext = hcontext;
    pgl->aguid = NULL;

    lRetCode = (mySCardListInterfacesA)(hcontext, pszCard, (LPGUID)&pgl->aguid,
        &pgl->cGuids);
    if (lRetCode!=SCARD_S_SUCCESS)
    {
        pgl->cGuids=0;
    }
    return lRetCode;
}

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _LocateCards(
  SCARDCONTEXT hcontext,
  STRINGLIST* mszCards,
  READERSTATELIST* prl
)
{
    LPCSTR pcstr=(0==strlen((LPCTSTR)mszCards->ac)) ? NULL : (LPCTSTR)mszCards->ac;

    return (mySCardLocateCardsA)(
                hcontext,
                pcstr,
                prl->ars,
                prl->cRStates);
}

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _RemoveReaderFromGroup(
  SCARDCONTEXT hcontext,
  char* szReaderName,
  char* szGroupName)
{
    return (mySCardRemoveReaderFromGroupA)(
                         hcontext,
                         szReaderName,
                         szGroupName);
}

#else

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _IntroduceReader(SCARDCONTEXT hcontext, char* szReaderName, char* szDeviceName)
{
    (void)hcontext;
    (void)szReaderName;
    (void)szDeviceName;
    return SCARD_E_UNSUPPORTED_FEATURE;
}

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _IntroduceReaderGroup(SCARDCONTEXT hcontext, char* szGroupName)
{
    (void)hcontext;
    (void)szGroupName;
    return SCARD_E_UNSUPPORTED_FEATURE;
}

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _ForgetReaderGroup(SCARDCONTEXT hcontext, char* szGroupName)
{
    (void)hcontext;
    (void)szGroupName;
    return SCARD_E_UNSUPPORTED_FEATURE;
}

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _AddReaderToGroup(
  SCARDCONTEXT hcontext,
  char* szReaderName,
  char* szGroupName)
{
    (void)hcontext;
    (void)szReaderName;
    (void)szGroupName;
    return SCARD_E_UNSUPPORTED_FEATURE;
}

///////////////////////////////////////////////////////////////////////////////
SCARDRETCODE _RemoveReaderFromGroup(
  SCARDCONTEXT hcontext,
  char* szReaderName,
  char* szGroupName)
{
    (void)hcontext;
    (void)szReaderName;
    (void)szGroupName;
    return SCARD_E_UNSUPPORTED_FEATURE;
}

#endif // WIN32


///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _IsValidContext(SCARDCONTEXT hcontext)
{
    return (mySCardIsValidContext)(hcontext);
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _GetAttrib(SCARDHANDLE hcard, SCARDDWORDARG dwAttrId, BYTELIST* pbl)
{
    long lRetCode;

    pbl->cBytes = 65535;
    pbl->ab = NULL;

    lRetCode = (mySCardGetAttrib)(hcard, dwAttrId, pbl->ab, &pbl->cBytes);
    if ((lRetCode!=SCARD_S_SUCCESS) || (pbl->cBytes<1))
    {
        return lRetCode;
    }

    pbl->ab = (unsigned char*)mem_Malloc(pbl->cBytes*sizeof(unsigned char));
    if (pbl->ab==NULL)
    {
        return SCARD_E_NO_MEMORY;
    }

    lRetCode = (mySCardGetAttrib)(hcard, dwAttrId, pbl->ab, &pbl->cBytes);
    return lRetCode;
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _SetAttrib(SCARDHANDLE hcard, SCARDDWORDARG dwAttrId, BYTELIST* pbl)
{
    long lRetCode;

    lRetCode = (mySCardSetAttrib)(hcard, dwAttrId, pbl->ab, pbl->cBytes);
    return lRetCode;
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _Control(
  SCARDHANDLE hcard,
  SCARDDWORDARG controlCode,
  BYTELIST* pblSendBuffer,
  BYTELIST* pblRecvBuffer
)
{
    SCARDRETCODE lRet;

    pblRecvBuffer->ab = (unsigned char*)mem_Malloc(MAX_BUFFER_SIZE_EXTENDED*sizeof(unsigned char));
    pblRecvBuffer->cBytes = MAX_BUFFER_SIZE_EXTENDED;

    lRet = (mySCardControl)(
                hcard,
                controlCode,
                pblSendBuffer->ab,
                pblSendBuffer->cBytes,
                pblRecvBuffer->ab,
                pblRecvBuffer->cBytes,
                &pblRecvBuffer->cBytes);
    return lRet;
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _BeginTransaction(SCARDHANDLE hcard)
{
    return (mySCardBeginTransaction)(hcard);
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _Cancel(SCARDCONTEXT hcontext)
{
    return (mySCardCancel)(hcontext);
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _Connect(
  SCARDCONTEXT hcontext,
  char* szReader,
  SCARDDWORDARG dwShareMode,
  SCARDDWORDARG dwPreferredProtocols,
  LPSCARDHANDLE phCard,
  SCARDDWORDARG* pdwActiveProtocol
)
{
    SCARDRETCODE lRet;

    lRet = (mySCardConnectA)(
            hcontext,
            (LPCTSTR)szReader,
            dwShareMode,
            dwPreferredProtocols,
            phCard,
            pdwActiveProtocol);

    return lRet;
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _Disconnect(SCARDHANDLE hcard, SCARDDWORDARG dwDisposition)
{
    return (mySCardDisconnect)(hcard, dwDisposition);
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _EndTransaction(SCARDHANDLE hcard, SCARDDWORDARG dwDisposition)
{
    return (mySCardEndTransaction)(hcard, dwDisposition);
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _EstablishContext(SCARDDWORDARG dwScope, SCARDCONTEXT* phContext)
{
    return (mySCardEstablishContext)(dwScope, NULL, NULL, phContext);
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _GetStatusChange(
    SCARDCONTEXT hcontext,
    SCARDDWORDARG dwTimeout,
    READERSTATELIST* prsl)
{
    SCARDRETCODE hresult;
    int i;

    // bad reader state list
    if (NULL==prsl)
    {
        return SCARD_E_INVALID_PARAMETER;
    }

    // remove changed bit
    for(i=0; i<prsl->cRStates; i++)
    {
        // remove changed bit
        prsl->ars[i].dwCurrentState = prsl->ars[i].dwCurrentState & (0xFFFFFFFF ^ SCARD_STATE_CHANGED);
    }

    hresult = (mySCardGetStatusChangeA)(hcontext, dwTimeout, prsl->ars,
        prsl->cRStates);

    //printf("\n%.8lx\n", hresult);
    //for(i=0; i<prsl->cRStates; i++)
    //{
    //    printf("%s %.8lx %.8lx\n", prsl->ars[i].szReader, prsl->ars[i].dwCurrentState, prsl->ars[i].dwEventState);
    //}

    return hresult;
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _ListReaders(
    SCARDCONTEXT hcontext,
    STRINGLIST* pmszGroups,
    STRINGLIST* pmszReaders)
{
    LPCTSTR mszGroups;
    SCARDDWORDARG cchReaders;
    LONG lRetCode;

    if (pmszGroups)
    {
        mszGroups=pmszGroups->ac;
    }
    else
    {
        mszGroups=NULL;
    }

    #ifdef NOAUTOALLOCATE
        // autoallocate memory; will be freed on output typemap
        cchReaders=SCARD_AUTOALLOCATE;

        pmszReaders->ac=NULL;
        pmszReaders->hcontext=hcontext;

        return (mySCardListReadersA)(hcontext, mszGroups,
            (LPTSTR)&pmszReaders->ac, &cchReaders);
    #endif //AUTOALLOCATE

    // no autoallocate on pcsc-lite; do a first call to get length
    // then allocate memory and do a final call
    #ifndef NOAUTOALLOCATE
        // set hcontext to 0 so that mem_Free will
        // be called instead of SCardFreeMemory
        pmszReaders->hcontext=0;
        pmszReaders->ac=NULL;
        cchReaders=0;

        lRetCode = (mySCardListReadersA)(hcontext, mszGroups, NULL,
            &cchReaders);

        if (SCARD_S_SUCCESS!=lRetCode)
        {
            return lRetCode;
        }

        if (0==cchReaders)
        {
            return SCARD_S_SUCCESS;
        }

        pmszReaders->ac=mem_Malloc(cchReaders*sizeof(char));
        if (NULL==pmszReaders->ac)
        {
            return SCARD_E_NO_MEMORY;
        }

        return (mySCardListReadersA)(hcontext, mszGroups, (LPTSTR)pmszReaders->ac, &cchReaders);
    #endif // !NOAUTOALLOCATE
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _ListReaderGroups(SCARDCONTEXT hcontext, STRINGLIST* pmszReaderGroups)
{
    DWORD cchReaderGroups;
    LONG lRetCode;

    #ifdef NOAUTOALLOCATE
        cchReaderGroups = SCARD_AUTOALLOCATE;
        pmszReaderGroups->ac=NULL;
        pmszReaderGroups->hcontext=hcontext;

        return (mySCardListReaderGroupsA)(hcontext,
            (LPTSTR)&pmszReaderGroups->ac, &cchReaderGroups);
    #endif // NOAUTOALLOCATE

    // no autoallocate on pcsc-lite; do a first call to get length
    // then allocate memory and do a final call
    #ifndef NOAUTOALLOCATE
        // set hcontext to 0 so that mem_Free will
        // be called instead of SCardFreeMemory

        pmszReaderGroups->hcontext=0;
        cchReaderGroups = 0;
        pmszReaderGroups->ac=NULL;
        lRetCode = (mySCardListReaderGroupsA)(hcontext,
            (LPTSTR)pmszReaderGroups->ac, &cchReaderGroups);
        if (SCARD_S_SUCCESS!=lRetCode)
        {
            return lRetCode;
        }

        if (0==cchReaderGroups)
        {
            return SCARD_S_SUCCESS;
        }

        pmszReaderGroups->ac=mem_Malloc(cchReaderGroups*sizeof(char));
        if (NULL==pmszReaderGroups->ac)
        {
            return SCARD_E_NO_MEMORY;
        }

        return (mySCardListReaderGroupsA)(hcontext, (LPTSTR)pmszReaderGroups->ac, &cchReaderGroups);
    #endif // !NOAUTOALLOCATE
};


///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _Reconnect(
    SCARDHANDLE hcard,
    SCARDDWORDARG dwShareMode,
    SCARDDWORDARG dwPreferredProtocols,
    SCARDDWORDARG dwInitialization,
    SCARDDWORDARG* pdwActiveProtocol
)
{
    return (mySCardReconnect)(
                               hcard,
                               dwShareMode,
                               dwPreferredProtocols,
                               dwInitialization,
                               pdwActiveProtocol);
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _ReleaseContext(SCARDCONTEXT hcontext)
{
    SCARDRETCODE lRet;
    lRet = (mySCardReleaseContext)(hcontext);
    return lRet;
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _Status(
  SCARDHANDLE hcard,
  STRING*  pszReaderName,
  SCARDDWORDARG* pdwState,
  SCARDDWORDARG* pdwProtocol,
  BYTELIST* pbl
)
{
    long lRetCode;
    SCARDDWORDARG dwReaderLen=256;
    SCARDDWORDARG dwAtrLen=36;

    for(;;)
    {
        pbl->ab = (unsigned char*)mem_Malloc(dwAtrLen*sizeof(unsigned char));
        if (pbl->ab == NULL)
        {
            lRetCode=SCARD_E_NO_MEMORY;
            break;
        }
        pbl->cBytes = dwAtrLen;
        pszReaderName->sz = mem_Malloc(dwReaderLen*sizeof(char));
        pszReaderName->hcontext = 0;
        if (NULL == pszReaderName->sz)
        {
            lRetCode=SCARD_E_NO_MEMORY;
            break;
        }
        pszReaderName->sz[0] = '\0';
        lRetCode = (mySCardStatusA)(
            hcard,
            (LPTSTR)pszReaderName->sz,
            &dwReaderLen,
            pdwState,
            pdwProtocol,
            pbl->ab,
            &pbl->cBytes);
        break;
    }

    return lRetCode;
}

///////////////////////////////////////////////////////////////////////////////
static SCARDRETCODE _Transmit(
  SCARDHANDLE hcard,
  unsigned long pioSendPci,
  BYTELIST* pblSendBuffer,
  BYTELIST* pblRecvBuffer
)
{
    PSCARD_IO_REQUEST piorequest=NULL;
    long ret;

    pblRecvBuffer->ab = (unsigned char*)mem_Malloc(MAX_BUFFER_SIZE_EXTENDED*sizeof(unsigned char));
    pblRecvBuffer->cBytes = MAX_BUFFER_SIZE_EXTENDED;

    // keep in sync with redefinition in PcscDefs.i
    switch(pioSendPci)
    {
        case SCARD_PROTOCOL_T0:
            piorequest = myg_prgSCardT0Pci;
            break;

        case SCARD_PROTOCOL_T1:
            piorequest = myg_prgSCardT1Pci;
            break;

        case SCARD_PROTOCOL_RAW:
        case SCARD_PROTOCOL_UNDEFINED:
            piorequest = myg_prgSCardRawPci;
            break;

        default:
            return SCARD_E_INVALID_PARAMETER;

    }
    ret = (mySCardTransmit)(
                hcard,
                piorequest,
                pblSendBuffer->ab,
                pblSendBuffer->cBytes,
                NULL,
                pblRecvBuffer->ab,
                &pblRecvBuffer->cBytes);

    return ret;
}

///////////////////////////////////////////////////////////////////////////////
static long _SCARD_CTL_CODE(long code)
{
    return SCARD_CTL_CODE(code);
}

///////////////////////////////////////////////////////////////////////////////
static ERRORSTRING _GetErrorMessage(long lErrCode)
{
    #ifdef WIN32
    #define _NO_SERVICE_MSG "The Smart card resource manager is not running."

        DWORD dwRetCode;
        LPVOID ppszError;

        dwRetCode=FormatMessage(
            FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_MAX_WIDTH_MASK,
            NULL,
            lErrCode,
            MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
            (LPTSTR)&ppszError,
            0,
            NULL);

        if (0L==dwRetCode)
        {
            ppszError=NULL;
            if (SCARD_E_NO_SERVICE==lErrCode)
            {
                ppszError=(LPVOID)LocalAlloc(LPTR, sizeof(_NO_SERVICE_MSG)+1);
                if (NULL!=ppszError)
                {
                    strncpy(ppszError, _NO_SERVICE_MSG, sizeof(_NO_SERVICE_MSG)+1);
                }
            }
        }

        return ppszError;
    #endif // WIN32
    #ifdef PCSCLITE
        return strdup(myPcscStringifyError(lErrCode));
    #endif // PCSCLITE
}

%}

//
// a few documentation typemaps
//
%typemap(doc, name="hcard", type="") (SCARDHANDLE hcard) "hcard: card handle return from SCardConnect()";
%typemap(doc, name="hcard", type="") (SCARDHANDLE* phcard) "hcard: on output, a card handle";

%typemap(doc, name="hcontext", type="") (SCARDCONTEXT hcontext) "hcontext: context handle return from SCardEstablishContext()";
%typemap(doc, name="hcontext", type="") (SCARDCONTEXT* phcontext) "hcontext: on output, a valid context handle if successful";

%typemap(doc, name="readerstatelist", type="tuple[]") (READERSTATELIST *prsl) "readerstatelist: in input/output, a list of reader state tuple (readername, state, atr)";

%typemap(doc, name="groupname", type="") (char* szGroupName) "groupname: card reader group name";
%typemap(doc, name="readername", type="") (char* szReaderName) "readername: card reader name";
%typemap(doc, name="cardname", type="") (char* szCardName) "cardname: friendly name of a card";
%typemap(doc, name="devicename", type="") (char* szDeviceName) "devicename: card reader device name";

%typemap(doc, name="providername", type="") (PROVIDERNAME_t* pszProviderName) "providername: on output, provider name";

%typemap(doc, name="readername", type="") (STRING* pszReaderNameOut) "readername: on output, reader name";

%typemap(doc, name="apducommand", type="byte[]") (BYTELIST* APDUCOMMAND) "apducommand: list of APDU bytes to transmit";
%typemap(doc, name="apduresponse", type="byte[]") (BYTELIST* APDURESPONSE) "apduresponse: on output, the list of APDU response bytes";
%typemap(doc, name="atr", type="byte[]") (BYTELIST* ATR) "atr: card ATR";
%typemap(doc, name="atr", type="byte[]") (BYTELIST* ATROUT) "atr: on output, the card ATR";
%typemap(doc, name="attributes", type="byte[]") (BYTELIST* ATTRIBUTES) "attributes: on output, a list of attributes";
%typemap(doc, name="mask", type="byte[]") (BYTELIST* MASK) "mask: mask to apply to card ATR";
%typemap(doc, name="inbuffer", type="byte[]") (BYTELIST* INBUFFER) "inbuffer: list of bytes to send with the control code";
%typemap(doc, name="outbuffer", type="byte[]") (BYTELIST* OUTBUFFER) "outbuffer: on output, the bytes returned by execution of the control code";

%typemap(doc, name="primaryprovider", type="GUID") (GUIDLIST* PRIMARYPROVIDER) "primaryprovidername: GUID of the smart card primary service provider";
%typemap(doc, name="providerlist", type="GUID[]") (GUIDLIST* PROVIDERLIST) "providerlist: list of GUIDs of interfaces supported by smart card";
%typemap(doc, name="interfaces", type="GUID[]") (GUIDLIST* GUIDINTERFACES) "interfaces: on output, a list of GUIDs of the interfaces supported by the smart card";

%typemap(doc, name="cards", type="") (STRINGLIST* CARDSTOLOCATE) "cards: a list of cards to locate";
%typemap(doc, name="matchingcards", type="[]") (STRINGLIST* MATCHINGCARDS) "matchingcards: on output, a list of matching cards";
%typemap(doc, name="readergroups", type="[]") (STRINGLIST* READERGROUPSIN) "readergroups: a list of reader groups to search for readers";
%typemap(doc, name="readergroups", type="[]") (STRINGLIST* READERGROUPSOUT) "readergroups: on output, the list of reader groups";
%typemap(doc, name="readers", type="[]") (STRINGLIST* READERSFOUND) "matchingcards: on output, a list of readers found";
%typemap(doc, name="readername", type="") (STRINGLIST* pszReaderName) "readername: on output, the name of the reader in which the card is inserted";

%typemap(doc, name="dwActiveProtocol", type="") (SCARDDWORDARG* pdwActiveProtocol) "dwActiveProtocol: on output, active protocol of card connection";
%typemap(doc, name="dwState", type="") (SCARDDWORDARG* pdwState) "dwState: on output, current state of the smart card";
%typemap(doc, name="dwProtocol", type="") (SCARDDWORDARG* pdwProtocol) "dwProtocol: on output, the current protocol";

%typemap(doc, name="dwScope", type="") (SCARDDWORDARG dwScope) "dwScope: context scope";
%typemap(doc, name="dwProviderId", type="") (SCARDDWORDARG dwProviderId) "dwProviderId: provider type, SCARD_PROVIDER_PRIMARY or SCARD_PROVIDER_CSP";
%typemap(doc, name="dwPreferredProtocols", type="") (SCARDDWORDARG dwPreferredProtocols) "dwPreferredProtocols: preferred protocols";
%typemap(doc, name="dwShareMode", type="") (SCARDDWORDARG dwShareMode) "dwShareMode: share mode";
%typemap(doc, name="dwDisposition", type="") (SCARDDWORDARG dwDisposition) "dwDisposition: card disposition on return";
%typemap(doc, name="dwAttrId", type="") (SCARDDWORDARG dwAttrId) "dwAttrId: value of attribute to get";
%typemap(doc, name="dwTimeout", type="") (SCARDDWORDARG dwTimeout) "dwTimeout: timeout value, INFINITE for infinite time-out";
%typemap(doc, name="dwInitialization", type="") (SCARDDWORDARG dwInitialization) "dwInitialization: the type of initialization that should be performed on the card";
%typemap(doc, name="dwControlCode", type="") (SCARDDWORDARG dwControlCode) "dwControlCode: the control code to send";


//
// these functions are only available on win32 PCSC
// but a fake function is provided on Unix
//

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_ADDREADERTOGROUP
"
adds a reader to a reader group

Windows only, not supported by PCSC lite wrapper.

example:

>>> from smartcard.scard import *
>>> ... establish context ...
>>> newgroup = 'SCard$MyOwnGroup'
>>> reader = 'SchlumbergerSema Reflex USB v.2 0'
>>> readeralias = 'SchlumbergerSema Reflex USB v.2 0 alias'
>>> hresult = SCardIntroduceReader(hcontext, readeralias, reader])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise error('Unable to introduce reader: ' +
>>>     SCardGetErrorMessage(hresult))
>>>
>>> hresult = SCardAddReaderToGroup(hcontext, readeralias, newgroup)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise error('Unable to add reader to group: ' +
>>>     SCardGetErrorMessage(hresult))
...
"
%enddef
%feature("docstring") DOCSTRING_ADDREADERTOGROUP;
%rename(SCardAddReaderToGroup) _AddReaderToGroup(
  SCARDCONTEXT hcontext,
  char* szReaderName,
  char* szGroupName);
SCARDRETCODE _AddReaderToGroup(
  SCARDCONTEXT hcontext,
  char* szReaderName,
  char* szGroupName);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_INTRODUCEREADER
"
Introduces a reader to the smart card subsystem.

Windows only, not supported by PCSC lite wrapper.

>>> from smartcard.scard import *
>>> ...
>>> dummyreader = readers[0] + ' dummy'
>>> hresult = SCardIntroduceReader(hcontext, dummyreader, readers[0])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise error('Unable to introduce reader: ' + dummyreader + ' : '
>>>     + SCardGetErrorMessage(hresult))
...
"
%enddef
%feature("docstring") DOCSTRING_INTRODUCEREADER;
%rename(SCardIntroduceReader) _IntroduceReader(SCARDCONTEXT hcontext, char* szReaderName, char* szDeviceName);
SCARDRETCODE _IntroduceReader(SCARDCONTEXT hcontext, char* szReaderName, char* szDeviceName);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_INTRODUCEREADERGROUP
"
Introduces a reader group to the smart card subsystem. However, the
reader group is not created until the group is specified when adding
a reader to the smart card database.

Windows only, not supported by PCSC lite wrapper.

>>> from smartcard.scard import *
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> hresult = SCardIntroduceReaderGroup(hcontext, 'SCard$MyOwnGroup')
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise error('Unable to introduce reader group: ' +
>>>     SCardGetErrorMessage(hresult))
>>> hresult = SCardAddReaderToGroup(hcontext, 'SchlumbergerSema Reflex USB v.2 0', 'SCard$MyOwnGroup')
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise error('Unable to add reader to group: ' +
>>>     SCardGetErrorMessage(hresult))
"
%enddef
%feature("docstring") DOCSTRING_INTRODUCEREADERGROUP;
%rename(SCardIntroduceReaderGroup) _IntroduceReaderGroup(SCARDCONTEXT hcontext, char* szGroupName);
SCARDRETCODE _IntroduceReaderGroup(SCARDCONTEXT hcontext, char* szGroupName);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_FORGETREADERGROUP
"
Removes a previously introduced smart card reader group from the smart
card subsystem. Although this function automatically clears all readers
from the group, it does not affect the existence of the individual readers
in the database.

Windows only, not supported by PCSC lite wrapper.

>>> from smartcard.scard import *
>>> ... establish context ...
>>> ...
>>> hresult = SCardForgetReaderGroup(hcontext, newgroup)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise error('Unable to forget reader group: ' +
>>>     SCardGetErrorMessage(hresult))
...
"
%enddef
%feature("docstring") DOCSTRING_FORGETREADERGROUP;
%rename(SCardForgetReaderGroup) _ForgetReaderGroup(SCARDCONTEXT hcontext, char* szGroupName);
SCARDRETCODE _ForgetReaderGroup(SCARDCONTEXT hcontext, char* szGroupName);

//
// these functions are only available on win32 PCSC
//

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_REMOVEREADERFROMGROUP
"

Removes a reader from an existing reader group.  This function has no
affect on the reader.

Windows only, not supported by PCSC lite wrapper.

>>> from smartcard.scard import *
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> hresult = SCardRemoveReaderFromGroup(hcontext, 'SchlumbergerSema Reflex USB v.2 0', 'SCard$MyOwnGroup')
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise error('Unable to remove reader from group: ' +
>>>     SCardGetErrorMessage(hresult))
...
"
%enddef
%feature("docstring") DOCSTRING_REMOVEREADERFROMGROUP;
%rename(SCardRemoveReaderFromGroup) _RemoveReaderFromGroup(
  SCARDCONTEXT hcontext,
  char* szReaderName,
  char* szGroupName);
SCARDRETCODE _RemoveReaderFromGroup(
  SCARDCONTEXT hcontext,
  char* szReaderName,
  char* szGroupName);

#ifdef WIN32
///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_FORGETCARDTYPE
"
removes an introduced smart card from the smart card subsystem.

Windows only, not supported by PCSC lite wrapper.

>>> from smartcard.scard import *
>>> ... establish context ...
>>> hresult = SCardForgetCardType(hcontext, 'myCardName')
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise error('Failed to remove card type: ' +
>>>     SCardGetErrorMessage(hresult))
...

"
%enddef
%feature("docstring") DOCSTRING_FORGETCARDTYPE;
%rename(SCardForgetCardType) _ForgetCardType(SCARDCONTEXT hcontext, char* szCardName);
SCARDRETCODE _ForgetCardType(SCARDCONTEXT hcontext, char* szCardName);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_FORGETREADER
"
Removes a previously introduced smart card reader from the smart
card subsystem.

Windows only, not supported by PCSC lite wrapper.

>>> from smartcard.scard import *
>>> ... establish context ...
>>> ...
>>> hresult = SCardForgetReader(hcontext, dummyreader)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise error('Failed to forget readers ' +
>>>     SCardGetErrorMessage(hresult))
...
"
%enddef
%feature("docstring") DOCSTRING_FORGETREADER;
%rename(SCardForgetReader) _ForgetReader(SCARDCONTEXT hcontext, char* szReaderName);
SCARDRETCODE _ForgetReader(SCARDCONTEXT hcontext, char* szReaderName);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_GETCARDTYPEPROVIDERNAME
"
Returns the name of the module (dynamic link library) containing the
provider for a given card name and provider type.

Windows only, not supported by PCSC lite wrapper.

>>> from smartcard.scard import *
>>> ... establish context ...
>>> hresult, cards = SCardListCards(hcontext, [], [])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise error('Failure to list cards: ' +
>>>     SCardGetErrorMessage(hresult))
>>> for i in cards:
>>>     hresult, providername = SCardGetCardTypeProviderName(hcontext, i, SCARD_PROVIDER_PRIMARY)
>>>     if hresult == SCARD_S_SUCCESS:
>>>          print(providername)
>>>     hresult, providername = SCardGetCardTypeProviderName(hcontext, i, SCARD_PROVIDER_CSP)
>>>     if hresult == SCARD_S_SUCCESS:
>>>          print(providername)
...
"
%enddef
%feature("docstring") DOCSTRING_GETCARDTYPEPROVIDERNAME;
%rename(SCardGetCardTypeProviderName) _GetCardTypeProviderName(
  SCARDCONTEXT hcontext,
  char* szCardName,
  SCARDDWORDARG dwProviderId,
  PROVIDERNAME_t* pszProviderName
);
SCARDRETCODE _GetCardTypeProviderName(
  SCARDCONTEXT hcontext,
  char* szCardName,
  SCARDDWORDARG dwProviderId,
  PROVIDERNAME_t* pszProviderName
);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_INTRODUCECARDTYPE
"
Introduces a smart card to the smart card subsystem (for the active user)
by adding it to the smart card database.

Windows only, not supported by PCSC lite wrapper.

>>> from smartcard.scard import *
>>> ...
>>> znewcardName = 'dummy-card'
>>> znewcardATR = [0x3B, 0x77, 0x94, 0x00, 0x00, 0x82, 0x30, 0x00, 0x13, 0x6C, 0x9F, 0x22]
>>> znewcardMask = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
>>> znewcardPrimGuid = smartcard.guid.strToGUID('{128F3806-4F70-4ccf-977A-60C390664840}')
>>> znewcardSecGuid = smartcard.guid.strToGUID('{EB7F69EA-BA20-47d0-8C50-11CFDEB63BBE}')
>>> ...
>>> hresult = SCardIntroduceCardType(hcontext, znewcardName,
>>>     znewcardPrimGuid, znewcardPrimGuid + znewcardSecGuid,
>>>     znewcardATR, znewcardMask)
>>>
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise error('Failed to introduce card type: ' +
>>>     SCardGetErrorMessage(hresult))
...
"
%enddef
%feature("docstring") DOCSTRING_INTRODUCECARDTYPE;
%rename(SCardIntroduceCardType) _IntroduceCardType(
  SCARDCONTEXT hcontext,
  char* szCardName,
  GUIDLIST* PRIMARYPROVIDER,
  GUIDLIST* PROVIDERLIST,
  BYTELIST* ATR,
  BYTELIST* MASK
);
SCARDRETCODE _IntroduceCardType(
  SCARDCONTEXT hcontext,
  char* szCardName,
  GUIDLIST* PRIMARYPROVIDER,
  GUIDLIST* PROVIDERLIST,
  BYTELIST* ATR,
  BYTELIST* MASK
);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_LISTINTERFACES
"
Provides a list of interfaces supplied by a given card.  The caller
supplies the name of a smart card previously introduced to the subsystem,
and receives the list of interfaces supported by the card

Windows only, not supported by PCSC lite wrapper.

>>> from smartcard.scard import *
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> hresult, interfaces = SCardListInterfaces(hcontext, 'Schlumberger Cryptoflex 8k v2')
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise error('Failed to list interfaces: ' +
>>>     SCardGetErrorMessage(hresult))
...
"
%enddef
%feature("docstring") DOCSTRING_LISTINTERFACES;
%rename(SCardListInterfaces) _ListInterfaces(SCARDCONTEXT hcontext, char* szCardName, GUIDLIST* GUIDINTERFACES);
SCARDRETCODE _ListInterfaces(SCARDCONTEXT hcontext, char* szCardName, GUIDLIST* GUIDINTERFACES);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_LISTCARDS
"
Searches the smart card database and provides a list of named cards
previously introduced to the system by the user.  The caller specifies an
ATR string, a set of interface identifiers (GUIDs), or both.  If both an
ATR string and an identifier array are supplied, the cards returned will
match the ATR string supplied and support the interfaces specified.

Windows only, not supported by PCSC lite wrapper.

>>> from smartcard.scard import *
>>> ...
>>> slbCryptoFlex8kv2ATR = [ 0x3B, 0x95, 0x15, 0x40, 0x00, 0x68, 0x01, 0x02, 0x00, 0x00  ]
>>> hresult, card = SCardListCards(hcontext, slbCryptoFlex8kv2ATR, [])
>>> if hresult ! =SCARD_S_SUCCESS:
>>>     raise error('Failure to locate Schlumberger Cryptoflex 8k v2 card: ' +
>>>     SCardGetErrorMessage(hresult))
>>> hresult, cards = SCardListCards(hcontext, [], [])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise error('Failure to list cards: ' +
>>>     SCardGetErrorMessage(hresult))
>>> print('Cards: ', cards)
...
"
%enddef
%feature("docstring") DOCSTRING_LISTCARDS;
%rename (SCardListCards) _ListCards(
    SCARDCONTEXT hcontext,
    BYTELIST* ATR,
    GUIDLIST* PROVIDERLIST,
    STRINGLIST* MATCHINGCARDS);
SCARDRETCODE _ListCards(
    SCARDCONTEXT hcontext,
    BYTELIST* ATR,
    GUIDLIST* PROVIDERLIST,
    STRINGLIST* MATCHINGCARDS);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_LOCATECARDS
"
Searches the readers listed in the readerstate parameter for a card
with an ATR string that matches one of the card names specified in
mszCards, returning immediately with the result.

Windows only, not supported by PCSC lite wrapper.

>>> from smartcard.scard import *
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> hresult, readers = SCardListReaders(hcontext, [])
>>> readerstates = []
>>> cards = ['Schlumberger Cryptoflex 4k', 'Schlumberger Cryptoflex 8k', 'Schlumberger Cryptoflex 8k v2']
>>> for i in xrange(len(readers)):
>>>     readerstates += [(readers[i], SCARD_STATE_UNAWARE)]
>>> hresult, newstates = SCardLocateCards(hcontext, cards, readerstates)
>>> for i in newstates:
>>>     reader, eventstate, atr = i
>>>     print(reader,)
>>>     for b in atr:
>>>         print('0x%.2X' % b, end='')
>>>     print("")
>>>     if eventstate & SCARD_STATE_ATRMATCH:
>>>         print('Card found')
>>>     if eventstate & SCARD_STATE_EMPTY:
>>>         print('Reader empty')
>>>     if eventstate & SCARD_STATE_PRESENT:
>>>         print('Card present in reader')
...
"
%enddef
%feature("docstring") DOCSTRING_LOCATECARDS;
%rename(SCardLocateCards) _LocateCards(
    SCARDCONTEXT hcontext,
    STRINGLIST* CARDSTOLOCATE,
    READERSTATELIST *prsl);
SCARDRETCODE _LocateCards(
    SCARDCONTEXT hcontext,
    STRINGLIST* CARDSTOLOCATE,
    READERSTATELIST *prsl);

#endif // WIN32

    ///////////////////////////////////////////////////////////////////////////////
    %define DOCSTRING_ISVALIDCONTEXT
    "
This function determines whether a smart card context handle is still
valid.  After a smart card context handle has been set by
L{SCardEstablishContext()}, it may become not valid if the resource manager
service has been shut down.

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> # valid context?
>>> hresult = SCardIsValidContext(hcontext)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
    "
    %enddef
    %feature("docstring") DOCSTRING_ISVALIDCONTEXT;
    %rename(SCardIsValidContext) _IsValidContext(SCARDCONTEXT hcontext);
    SCARDRETCODE _IsValidContext(SCARDCONTEXT hcontext);

    ///////////////////////////////////////////////////////////////////////////////
    %define DOCSTRING_GETATTRIB
    "
This function get an attribute from the IFD Handler.

The possible attributes are::
    ======================================== ======= =======
    Attribute                                Windows  PCSC
                                                      lite
    ======================================== ======= =======
    SCARD_ATTR_ASYNC_PROTOCOL_TYPES                     Y
    SCARD_ATTR_ATR_STRING                       Y       Y
    SCARD_ATTR_CHANNEL_ID                       Y       Y
    SCARD_ATTR_CHARACTERISTICS                  Y       Y
    SCARD_ATTR_CURRENT_BWT                      Y       Y
    SCARD_ATTR_CURRENT_CLK                      Y       Y
    SCARD_ATTR_CURRENT_CWT                      Y       Y
    SCARD_ATTR_CURRENT_D                        Y       Y
    SCARD_ATTR_CURRENT_EBC_ENCODING             Y       Y
    SCARD_ATTR_CURRENT_F                        Y       Y
    SCARD_ATTR_CURRENT_IFSC                     Y       Y
    SCARD_ATTR_CURRENT_IFSD                     Y       Y
    SCARD_ATTR_CURRENT_IO_STATE                 Y       Y
    SCARD_ATTR_CURRENT_N                        Y       Y
    SCARD_ATTR_CURRENT_PROTOCOL_TYPE            Y       Y
    SCARD_ATTR_CURRENT_W                        Y       Y
    SCARD_ATTR_DEFAULT_CLK                      Y       Y
    SCARD_ATTR_DEFAULT_DATA_RATE                Y       Y
    SCARD_ATTR_DEVICE_FRIENDLY_NAME_A           Y       Y
    SCARD_ATTR_DEVICE_FRIENDLY_NAME_W           Y       Y
    SCARD_ATTR_DEVICE_IN_USE                    Y       Y
    SCARD_ATTR_DEVICE_SYSTEM_NAME_A             Y       Y
    SCARD_ATTR_DEVICE_SYSTEM_NAME_W             Y       Y
    SCARD_ATTR_DEVICE_UNIT                      Y       Y
    SCARD_ATTR_ESC_AUTHREQUEST                  Y       Y
    SCARD_ATTR_ESC_CANCEL                       Y       Y
    SCARD_ATTR_ESC_RESET                        Y       Y
    SCARD_ATTR_EXTENDED_BWT                     Y       Y
    SCARD_ATTR_ICC_INTERFACE_STATUS             Y       Y
    SCARD_ATTR_ICC_PRESENCE                     Y       Y
    SCARD_ATTR_ICC_TYPE_PER_ATR                 Y       Y
    SCARD_ATTR_MAXINPUT                         Y       Y
    SCARD_ATTR_MAX_CLK                          Y       Y
    SCARD_ATTR_MAX_DATA_RATE                    Y       Y
    SCARD_ATTR_MAX_IFSD                         Y       Y
    SCARD_ATTR_POWER_MGMT_SUPPORT               Y       Y
    SCARD_ATTR_SUPRESS_T1_IFS_REQUEST           Y       Y
    SCARD_ATTR_SYNC_PROTOCOL_TYPES                      Y
    SCARD_ATTR_USER_AUTH_INPUT_DEVICE           Y       Y
    SCARD_ATTR_USER_TO_CARD_AUTH_DEVICE         Y       Y
    SCARD_ATTR_VENDOR_IFD_SERIAL_NO             Y       Y
    SCARD_ATTR_VENDOR_IFD_TYPE                  Y       Y
    SCARD_ATTR_VENDOR_IFD_VERSION               Y       Y
    SCARD_ATTR_VENDOR_NAME                      Y       Y
    ======================================== ======= =======

Not all the dwAttrId values listed above may be implemented in the IFD
Handler you are using.  And some dwAttrId values not listed here may be
implemented.

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> # list readers
>>> hresult, readers = SCardListReaders(hcontext, [])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.ListReadersException(hresult)
>>>
>>> # connect
>>> hresult, hcard, dwActiveProtocol = SCardConnect(
>>>     hcontext, readers[0], SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>>
>>> # get attribute
>>> hresult, attrib = SCardGetAttrib(hcard, SCARD_ATTR_ATR_STRING)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>> print(attrib)
    "
    %enddef
    %feature("docstring") DOCSTRING_GETATTRIB;
    %rename(SCardGetAttrib) _GetAttrib(SCARDHANDLE hcard, SCARDDWORDARG dwAttrId, BYTELIST* ATTRIBUTES);
    SCARDRETCODE _GetAttrib(SCARDHANDLE hcard, SCARDDWORDARG dwAttrId, BYTELIST* ATTRIBUTES);

    ///////////////////////////////////////////////////////////////////////////////
    %define DOCSTRING_SETATTRIB
    "
This function sets an attribute from the IFD Handler. Not all
attributes are supported by all readers nor can they be set at all
times.

The possible attributes are::
    ======================================== ======= =======
    Attribute                                Windows  PCSC
                                                      lite
    ======================================== ======= =======
    SCARD_ATTR_ASYNC_PROTOCOL_TYPES                     Y
    SCARD_ATTR_ATR_STRING                       Y       Y
    SCARD_ATTR_CHANNEL_ID                       Y       Y
    SCARD_ATTR_CHARACTERISTICS                  Y       Y
    SCARD_ATTR_CURRENT_BWT                      Y       Y
    SCARD_ATTR_CURRENT_CLK                      Y       Y
    SCARD_ATTR_CURRENT_CWT                      Y       Y
    SCARD_ATTR_CURRENT_D                        Y       Y
    SCARD_ATTR_CURRENT_EBC_ENCODING             Y       Y
    SCARD_ATTR_CURRENT_F                        Y       Y
    SCARD_ATTR_CURRENT_IFSC                     Y       Y
    SCARD_ATTR_CURRENT_IFSD                     Y       Y
    SCARD_ATTR_CURRENT_IO_STATE                 Y       Y
    SCARD_ATTR_CURRENT_N                        Y       Y
    SCARD_ATTR_CURRENT_PROTOCOL_TYPE            Y       Y
    SCARD_ATTR_CURRENT_W                        Y       Y
    SCARD_ATTR_DEFAULT_CLK                      Y       Y
    SCARD_ATTR_DEFAULT_DATA_RATE                Y       Y
    SCARD_ATTR_DEVICE_FRIENDLY_NAME_A           Y       Y
    SCARD_ATTR_DEVICE_FRIENDLY_NAME_W           Y       Y
    SCARD_ATTR_DEVICE_IN_USE                    Y       Y
    SCARD_ATTR_DEVICE_SYSTEM_NAME_A             Y       Y
    SCARD_ATTR_DEVICE_SYSTEM_NAME_W             Y       Y
    SCARD_ATTR_DEVICE_UNIT                      Y       Y
    SCARD_ATTR_ESC_AUTHREQUEST                  Y       Y
    SCARD_ATTR_ESC_CANCEL                       Y       Y
    SCARD_ATTR_ESC_RESET                        Y       Y
    SCARD_ATTR_EXTENDED_BWT                     Y       Y
    SCARD_ATTR_ICC_INTERFACE_STATUS             Y       Y
    SCARD_ATTR_ICC_PRESENCE                     Y       Y
    SCARD_ATTR_ICC_TYPE_PER_ATR                 Y       Y
    SCARD_ATTR_MAXINPUT                         Y       Y
    SCARD_ATTR_MAX_CLK                          Y       Y
    SCARD_ATTR_MAX_DATA_RATE                    Y       Y
    SCARD_ATTR_MAX_IFSD                         Y       Y
    SCARD_ATTR_POWER_MGMT_SUPPORT               Y       Y
    SCARD_ATTR_SUPRESS_T1_IFS_REQUEST           Y       Y
    SCARD_ATTR_SYNC_PROTOCOL_TYPES                      Y
    SCARD_ATTR_USER_AUTH_INPUT_DEVICE           Y       Y
    SCARD_ATTR_USER_TO_CARD_AUTH_DEVICE         Y       Y
    SCARD_ATTR_VENDOR_IFD_SERIAL_NO             Y       Y
    SCARD_ATTR_VENDOR_IFD_TYPE                  Y       Y
    SCARD_ATTR_VENDOR_IFD_VERSION               Y       Y
    SCARD_ATTR_VENDOR_NAME                      Y       Y
    ======================================== ======= =======

Not all the dwAttrId values listed above may be implemented in the
IFD Handler you are using.  And some dwAttrId values not listed here
may be implemented.

>>> from smartcard.scard import *
>>> ... establish context and connect to card ...
>>> hresult, attrib = SCardSetAttrib(hcard, SCARD_ATTR_VENDOR_NAME, ['G', 'e', 'm', 'a', 'l', 't', 'o'])
>>> if hresult != SCARD_S_SUCCESS:
>>>      print('Failed to set attribute')
>>> ...
    "
    %enddef
    %feature("docstring") DOCSTRING_SETATTRIB;
    %rename(SCardSetAttrib) _SetAttrib(SCARDHANDLE hcard, SCARDDWORDARG dwAttrId, BYTELIST* ATTRIBUTESIN);
    SCARDRETCODE _SetAttrib(SCARDHANDLE hcard, SCARDDWORDARG dwAttrId, BYTELIST* ATTRIBUTESIN);


    ///////////////////////////////////////////////////////////////////////////////
    %define DOCSTRING_CONTROL
    "
This function sends a control command to the reader connected to by
L{SCardConnect()}.  It returns a result and the control response.

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> # list readers
>>> hresult, readers = SCardListReaders(hcontext, [])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.ListReadersException(hresult)
>>>
>>> # connect
>>> hresult, hcard, dwActiveProtocol = SCardConnect(
>>>     hcontext, readers[0], SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>>
>>> # control
>>> CMD = [0x12, 0x34]
>>> hresult, response = SCardControl(hcard, 42, CMD)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
    "
    %enddef
    %feature("docstring") DOCSTRING_CONTROL;
    %rename(SCardControl) _Control(
      SCARDHANDLE hcard,
      SCARDDWORDARG dwControlCode,
      BYTELIST* INBUFFER,
      BYTELIST* OUTBUFFER
   );
    SCARDRETCODE _Control(
      SCARDHANDLE hcard,
      SCARDDWORDARG dwControlCode,
      BYTELIST* INBUFFER,
      BYTELIST* OUTBUFFER
   );


///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_BEGINTRANSACTION
"
This function establishes a temporary exclusive access mode for doing a
series of commands or transaction.  You might want to use this when you
are selecting a few files and then writing a large file so you can make
sure that another application will not change the current file.

If another application has a lock on this reader or this application is
in SCARD_SHARE_EXCLUSIVE there will be no action taken.

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> # list readers
>>> hresult, readers = SCardListReaders(hcontext, [])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.ListReadersException(hresult)
>>>
>>> # connect
>>> hresult, hcard, dwActiveProtocol = SCardConnect(
>>>     hcontext, readers[0], SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>>
>>> # begin transaction
>>> hresult = SCardBeginTransaction(hcard)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
"
%enddef
%feature("docstring") DOCSTRING_BEGINTRANSACTION;
%rename(SCardBeginTransaction) _BeginTransaction(SCARDHANDLE hcard);
SCARDRETCODE _BeginTransaction(SCARDHANDLE hcard);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_CANCEL
"
This function cancels all pending blocking requests on the
L{SCardGetStatusChange()} function.

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>> ... establish context ...
>>> hresult = SCardCancel(hcard)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
..."
%enddef
%feature("docstring") DOCSTRING_CANCEL;
%rename(SCardCancel) _Cancel(SCARDCONTEXT hcontext);
SCARDRETCODE _Cancel(SCARDCONTEXT hcontext);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_CONNECT
"
This function establishes a connection to the friendly name of the reader
specified in readername.  The first connection will power up and
perform a reset on the card.

Value of dwShareMode:
 - SCARD_SHARE_SHARED      This application will allow others to share the reader
 - SCARD_SHARE_EXCLUSIVE   This application will NOT allow others to share the reader
 - SCARD_SHARE_DIRECT      Direct control of the reader, even without a card

SCARD_SHARE_DIRECT can be used before using L{SCardControl()} to
send control commands to the reader even if a card is not present in
the reader.

Value of dwPreferredProtocols:
 - SCARD_PROTOCOL_T0               Use the T=0 protocol
 - SCARD_PROTOCOL_T1               Use the T=1 protocol
 - SCARD_PROTOCOL_RAW              Use with memory type cards

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> # list readers
>>> hresult, readers = SCardListReaders(hcontext, [])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.ListReadersException(hresult)
>>>
>>> # connect
>>> hresult, hcard, dwActiveProtocol = SCardConnect(
>>>     hcontext, readers[0], SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
"
%enddef
%feature("docstring") DOCSTRING_CONNECT;
%rename(SCardConnect) _Connect(
  SCARDCONTEXT hcontext,
  char* szReaderName,
  SCARDDWORDARG dwShareMode,
  SCARDDWORDARG dwPreferredProtocols,
  SCARDHANDLE* phcard,
  SCARDDWORDARG* pdwActiveProtocol
);
SCARDRETCODE _Connect(
  SCARDCONTEXT hcontext,
  char* szReaderName,
  SCARDDWORDARG dwShareMode,
  SCARDDWORDARG dwPreferredProtocols,
  SCARDHANDLE* phcard,
  SCARDDWORDARG* pdwActiveProtocol
);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_DISCONNECT
"
This function terminates a connection to the connection made through
L{SCardConnect()}.

Value of disposition:
 - SCARD_LEAVE_CARD        Do nothing
 - SCARD_RESET_CARD        Reset the card (warm reset)
 - SCARD_UNPOWER_CARD      Unpower the card (cold reset)
 - SCARD_EJECT_CARD        Eject the card

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> # list readers
>>> hresult, readers = SCardListReaders(hcontext, [])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.ListReadersException(hresult)
>>>
>>> # connect
>>> hresult, hcard, dwActiveProtocol = SCardConnect(
>>>     hcontext, readers[0], SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>>
>>> # disconnect
>>> hresult = SCardDisconnect(hcard, SCARD_UNPOWER_CARD)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
"
%enddef
%feature("docstring") DOCSTRING_DISCONNECT;
%rename(SCardDisconnect) _Disconnect(SCARDHANDLE hcard, SCARDDWORDARG dwDisposition);
SCARDRETCODE _Disconnect(SCARDHANDLE hcard, SCARDDWORDARG dwDisposition);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_ENDTRANSACTION
"
This function ends a previously begun transaction.  The calling
application must be the owner of the previously begun transaction or an
error will occur.

Value of disposition:
 - SCARD_LEAVE_CARD        Do nothing
 - SCARD_RESET_CARD        Reset the card
 - SCARD_UNPOWER_CARD      Unpower the card
 - SCARD_EJECT_CARD        Eject the card

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> # list readers
>>> hresult, readers = SCardListReaders(hcontext, [])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.ListReadersException(hresult)
>>>
>>> # connect
>>> hresult, hcard, dwActiveProtocol = SCardConnect(
>>>     hcontext, readers[0], SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>>
>>> # begin transaction
>>> hresult = SCardBeginTransaction(hcard)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>>
>>> # end transaction
>>> hresult = SCardEndTransaction(hcard, SCARD_LEAVE_CARD)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
"
%enddef
%feature("docstring") DOCSTRING_ENDTRANSACTION;
%rename(SCardEndTransaction) _EndTransaction(SCARDHANDLE hcard, SCARDDWORDARG dwDisposition);
SCARDRETCODE _EndTransaction(SCARDHANDLE hcard, SCARDDWORDARG dwDisposition);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_ESTABLISHCONTEXT
"
This function creates a communication context to the PC/SC Resource
Manager.  This must be the first PC/SC function called in a PC/SC application.

Value of dwScope:
 - SCARD_SCOPE_USER        Operations performed within the scope of the User
 - SCARD_SCOPE_TERMINAL    Not used
 - SCARD_SCOPE_GLOBAL      Not used
 - SCARD_SCOPE_SYSTEM      Operations performed within the scope of the system

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
"
%enddef
%feature("docstring") DOCSTRING_ESTABLISHCONTEXT;
%rename(SCardEstablishContext) _EstablishContext(SCARDDWORDARG dwScope, SCARDCONTEXT* phcontext);
SCARDRETCODE _EstablishContext(SCARDDWORDARG dwScope, SCARDCONTEXT* phcontext);


///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_GETSTATUSCHANGE
"
This function receives a structure or list of tuples containing reader
states. A READERSTATE hast three fields (readername, state, atr).
It then blocks for a change in state to occur on any of the OR'd
values contained in the current state for a maximum blocking time of
dwTimeout or forever if INFINITE is used.  The new event state will be
contained in state.  A status change might be a card insertion or
removal event, a change in ATR, etc.

Value of state:
 - SCARD_STATE_UNAWARE         The application is unaware of the current state, and would like to know. The use of this value results in an immediate return from state transition monitoring services. This is represented by all bits set to zero
 - SCARD_STATE_IGNORE          This reader should be ignored
 - SCARD_STATE_CHANGED         There is a difference between the state believed by the application, and the state known by the resource manager. When this bit is set, the application may assume a significant state change has occurred on this reader
 - SCARD_STATE_UNKNOWN         The given reader name is not recognized by the resource manager. If this bit is set, then SCARD_STATE_CHANGED and SCARD_STATE_IGNORE will also be set
 - SCARD_STATE_UNAVAILABLE     The actual state of this reader is not available. If this bit is set, then all the following bits are clear
 - SCARD_STATE_EMPTY           There is no card in the reader. If this bit is set, all the following bits will be clear
 - SCARD_STATE_PRESENT         There is a card in the reader
 - SCARD_STATE_ATRMATCH        There is a card in the reader with an ATR matching one of the target cards. If this bit is set, SCARD_STATE_PRESENT will also be set. This bit is only returned on the SCardLocateCards function
 - SCARD_STATE_EXCLUSIVE       The card in the reader is allocated for exclusive use by another application. If this bit is set, SCARD_STATE_PRESENT will also be set
 - SCARD_STATE_INUSE           The card in the reader is in use by one or more other applications, but may be connected to in shared mode. If this bit is set, SCARD_STATE_PRESENT will also be set
 - SCARD_STATE_MUTE            There is an unresponsive card in the reader

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> # list readers
>>> hresult, readers = SCardListReaders(hcontext, [])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.ListReadersException(hresult)
>>>
>>> # get status change
>>> readerstates = []
>>> for reader in readers:
>>>     readerstates.append((reader, SCARD_STATE_UNAWARE))
>>>
>>> hresult, newstates = SCardGetStatusChange(hcontext, INFINITE, readerstates)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>> for state in newstates:
>>>     reader, eventstate, atr = state
>>>     print(f'Reader: {reader}:', end='')
>>>     if eventstate & SCARD_STATE_PRESENT:
>>>         print(' Card present')
>>>     if eventstate & SCARD_STATE_EMPTY:
>>>         print(' Reader empty')
>>>
>>> print('insert or remove a card')
>>> # wait for card move
>>> readerstates = newstates
>>> hresult, newstates = SCardGetStatusChange(hcontext, INFINITE, readerstates)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
"
%enddef
%feature("docstring") DOCSTRING_GETSTATUSCHANGE;
%rename(SCardGetStatusChange) _GetStatusChange(
    SCARDCONTEXT hcontext,
    SCARDDWORDARG dwTimeout,
    READERSTATELIST* prsl);
SCARDRETCODE _GetStatusChange(
    SCARDCONTEXT hcontext,
    SCARDDWORDARG dwTimeout,
    READERSTATELIST* prsl);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_LISTREADERS
"
This function returns a list of currently available readers on the system.
A list of group can be provided in input to list readers in a given
group only.

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> # list readers
>>> hresult, readers = SCardListReaders(hcontext, [])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.ListReadersException(hresult)
>>> for reader in readers:
>>>     print(reader)
"
%enddef
%feature("docstring") DOCSTRING_LISTREADERS;
%rename(SCardListReaders) _ListReaders(
    SCARDCONTEXT hcontext,
    STRINGLIST* READERGROUPSIN,
    STRINGLIST* READERSFOUND);
SCARDRETCODE _ListReaders(
    SCARDCONTEXT hcontext,
    STRINGLIST* READERGROUPSIN,
    STRINGLIST* READERSFOUND);


///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_LISTREADERGROUPS
"
This function returns a list of currently available reader groups on the
system.

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> hresult, readerGroups = SCardListReaderGroups(hcontext)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>> print('PCSC Reader groups:', readerGroups)
"
%enddef
%feature("docstring") DOCSTRING_LISTREADERGROUPS;
%rename(SCardListReaderGroups) _ListReaderGroups(SCARDCONTEXT hcontext, STRINGLIST* READERGROUPSOUT);
SCARDRETCODE _ListReaderGroups(SCARDCONTEXT hcontext, STRINGLIST* READERGROUPSOUT);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_RECONNECT
"
This function reestablishes a connection to a reader that was previously
connected to using L{SCardConnect()}.  In a multi application environment it
is possible for an application to reset the card in shared mode.  When
this occurs any other application trying to access certain commands will
be returned the value SCARD_W_RESET_CARD.  When this occurs
L{SCardReconnect()} must be called in order to acknowledge that the card was
reset and allow it to change it's state accordingly.

Value of dwShareMode:
 - SCARD_SHARE_SHARED      This application will allow others to share the reader
 - SCARD_SHARE_EXCLUSIVE   This application will NOT allow others to share the reader

Value of dwPreferredProtocols:
 - SCARD_PROTOCOL_T0               Use the T=0 protocol
 - SCARD_PROTOCOL_T1               Use the T=1 protocol
 - SCARD_PROTOCOL_RAW              Use with memory type cards

dwPreferredProtocols is a bit mask of acceptable protocols for the connection. You can use (SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1) if you do not have a preferred protocol.

Value of dwInitialization:
 - SCARD_LEAVE_CARD            Do nothing
 - SCARD_RESET_CARD            Reset the card (warm reset)
 - SCARD_UNPOWER_CARD          Unpower the card (cold reset)
 - SCARD_EJECT_CARD            Eject the card

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> # list readers
>>> hresult, readers = SCardListReaders(hcontext, [])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.ListReadersException(hresult)
>>>
>>> # connect
>>> hresult, hcard, dwActiveProtocol = SCardConnect(
>>>     hcontext, readers[0], SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>>
>>> # reconnect
>>> hresult, activeProtocol = SCardReconnect(hcard, SCARD_SHARE_EXCLUSIVE, SCARD_PROTOCOL_T0, SCARD_RESET_CARD)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
"
%enddef
%feature("docstring") DOCSTRING_RECONNECT;
%rename(SCardReconnect) _Reconnect(
  SCARDHANDLE hcard,
  SCARDDWORDARG dwShareMode,
  SCARDDWORDARG dwPreferredProtocols,
  SCARDDWORDARG dwInitialization,
  SCARDDWORDARG* pdwActiveProtocol
);
SCARDRETCODE _Reconnect(
  SCARDHANDLE hcard,
  SCARDDWORDARG dwShareMode,
  SCARDDWORDARG dwPreferredProtocols,
  SCARDDWORDARG dwInitialization,
  SCARDDWORDARG* pdwActiveProtocol
);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_RELEASECONTEXT
"
Release a PC/SC context established by L{SCardEstablishContext()}.

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> # release context
>>> hresult = SCardReleaseContext(hcontext)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.ReleaseContextException(hresult)
"
%enddef
%feature("docstring") DOCSTRING_RELEASECONTEXT;
%rename(SCardReleaseContext) _ReleaseContext(SCARDCONTEXT hcontext);
SCARDRETCODE _ReleaseContext(SCARDCONTEXT hcontext);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_STATUS
"
This function returns the current status of the reader connected to by
hcard.  The reader friendly name is returned, as well as the state,
protocol and ATR.  The state is a DWORD possibly OR'd with the following
values:

Value of pdwState:
 - SCARD_ABSENT        There is no card in the reader
 - SCARD_PRESENT       There is a card in the reader, but it has not been moved into position for use
 - SCARD_SWALLOWED     There is a card in the reader in position for use. The card is not powered
 - SCARD_POWERED       Power is being provided to the card, but the reader driver is unaware of the mode of the card
 - SCARD_NEGOTIABLE    The card has been reset and is awaiting PTS negotiation
 - SCARD_SPECIFIC      The card has been reset and specific communication protocols have been established

Value of pdwProtocol:
 - SCARD_PROTOCOL_T0       Use the T=0 protocol
 - SCARD_PROTOCOL_T1       Use the T=1 protocol

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>> from smartcard.util import toHexString
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> # list readers
>>> hresult, readers = SCardListReaders(hcontext, [])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.ListReadersException(hresult)
>>>
>>> # connect
>>> hresult, hcard, dwActiveProtocol = SCardConnect(
>>>     hcontext, readers[0], SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>>
>>> # status
>>> hresult, reader, state, protocol, atr = SCardStatus(hcard)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>> print('Reader:', reader)
>>> print('State: 0x%04X' % state)
>>> print('Protocol:', protocol)
>>> print('ATR:', toHexString(atr))
"
%enddef
%feature("docstring") DOCSTRING_STATUS;
%rename(SCardStatus) _Status(
  SCARDHANDLE hcard,
  STRING* pszReaderNameOut,
  SCARDDWORDARG* pdwState,
  SCARDDWORDARG* pdwProtocol,
  BYTELIST* ATROUT
);
SCARDRETCODE _Status(
  SCARDHANDLE hcard,
  STRING* pszReaderNameOut,
  SCARDDWORDARG* pdwState,
  SCARDDWORDARG* pdwProtocol,
  BYTELIST* ATROUT
);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_TRANSMIT
"
This function sends an APDU to the smart card contained in the reader
connected to by L{SCardConnect()}.
It returns a result and the card APDU response.

Value of pioSendPci:
 - SCARD_PCI_T0            Pre-defined T=0 PCI structure
 - SCARD_PCI_T1            Pre-defined T=1 PCI structure

>>> from smartcard.scard import *
>>> from smartcard.pcsc import *
>>> from smartcard.util import toHexString
>>>
>>> # establish context
>>> hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.EstablishContextException(hresult)
>>>
>>> # list readers
>>> hresult, readers = SCardListReaders(hcontext, [])
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.ListReadersException(hresult)
>>>
>>> # connect
>>> hresult, hcard, dwActiveProtocol = SCardConnect(
>>>     hcontext, readers[0], SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>>
>>> # transmit
>>> SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
>>> DF_TELECOM = [0x7F, 0x10]
>>> hresult, response = SCardTransmit(hcard, SCARD_PCI_T0, SELECT + DF_TELECOM)
>>> if hresult != SCARD_S_SUCCESS:
>>>     raise PCSCExceptions.BaseSCardException(hresult)
>>> print(toHexString(response))
"
%enddef
%feature("docstring") DOCSTRING_TRANSMIT;
%rename(SCardTransmit) _Transmit(
  SCARDHANDLE hcard,
  unsigned long pioSendPci,
  BYTELIST* APDUCOMMAND,
  BYTELIST* APDURESPONSE
);
SCARDRETCODE _Transmit(
  SCARDHANDLE hcard,
  unsigned long pioSendPci,
  BYTELIST* APDUCOMMAND,
  BYTELIST* APDURESPONSE
);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_SCARD_CTL_CODE
"
This function returns the value of a control code

>>> from smartcard.scard import *
>>> ...
>>> CM_IOCTL_GET_FEATURE_REQUEST = SCARD_CTL_CODE(3400)
>>> ...
"
%enddef
%feature("docstring") DOCSTRING_SCARD_CTL_CODE;
%rename(SCARD_CTL_CODE) _SCARD_CTL_CODE(long code);
long _SCARD_CTL_CODE(long code);

///////////////////////////////////////////////////////////////////////////////
%define DOCSTRING_GETERRORMESSAGE
"
This function return a human readable text for the given PC/SC error code.

>>> from smartcard.scard import *
>>> ...
>>> hresult, response = SCardTransmit(hcard, SCARD_PCI_T0, SELECT + DF_TELECOM)
>>> if hresult != SCARD_S_SUCCESS:
>>>     print('Failed to transmit:', SCardGetErrorMessage(hresult))
>>> ...
"
%enddef
%feature("docstring") DOCSTRING_GETERRORMESSAGE;
%rename(SCardGetErrorMessage) _GetErrorMessage(long lErrCode);
ERRORSTRING _GetErrorMessage(long lErrCode);


%inline
%{
%}

%{
    PyObject *PyExc_SCardError=NULL;
%}


//----------------------------------------------------------------------
// This code gets added to the module initialization function
//----------------------------------------------------------------------
%init
%{
    PyExc_SCardError = PyErr_NewException("scard.error", NULL, NULL);
    if (PyExc_SCardError != NULL)
            PyDict_SetItemString(d, "error", PyExc_SCardError);

    /* load the PCSC library */
    winscard_init();
%}

//----------------------------------------------------------------------
// This code is added to the scard.py python module
//----------------------------------------------------------------------
%pythoncode %{
    error = _scard.error
%}

%include PcscDefs.i

#ifdef PCSCLITEyy
%pythoncode %{

def SCardListCards(hcontext, atr, guidlist):
    return (SCARD_S_SUCCESS, [])

def SCardLocateCards(hcontext, cardnames, readerstates):
    newreaderstates=[]
    for state in readerstates:
        newreaderstates.append((state[0], state[1], []))

    return (SCARD_S_SUCCESS, newreaderstates)
%}
#endif

#ifdef PCSCLITE
%constant char* resourceManager = "pcsclite" ;
    #ifdef __APPLE__
        %constant char* resourceManagerSubType = "pcsclite-lion" ;
    #else // !__APPLE__
        %constant char* resourceManagerSubType = "pcsclite-linux" ;
    #endif // __APPLE__
#endif // PCSCLITE
#ifdef WIN32
%constant char* resourceManager = "winscard" ;
%constant char* resourceManagerSubType = "winscard-win32" ;
#endif // WIN32
