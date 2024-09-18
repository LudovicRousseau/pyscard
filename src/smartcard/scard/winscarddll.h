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

#ifndef __WINSCARDDLL_H__
#define __WINSCARDDLL_H__

#ifdef WIN32
    #include <windows.h>
#endif

#ifdef __APPLE__
    #include <PCSC/wintypes.h>
    #include <PCSC/winscard.h>
    #define LPCTSTR char*
#else // !__APPLE__
    #include <winscard.h>
#endif

#ifdef PCSCLITE
    #define WINSCARDAPI
    #define WINAPI
    #define IN
    #define OUT
    #define LPSCARD_READERSTATEA SCARD_READERSTATE *
    #define SCARD_AUTOALLOCATE (DWORD)(-1)
    #ifndef FALSE
        #define FALSE (0==1)
    #endif // FALSE
    #ifndef TRUE
        #define TRUE (1==1)
    #endif
#endif // PCSCLITE

//
// these functions are only available on win32 PCSC
//
#ifdef WIN32
    typedef WINSCARDAPI HANDLE
    (WINAPI *SCARDACCESSSTARTEDEVENT)(void);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDADDREADERTOGROUPA)(
        IN SCARDCONTEXT hContext,
        IN LPCTSTR szReaderName,
        IN LPCTSTR szGroupName);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDFORGETCARDTYPEA)(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szCardName);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDFORGETREADERA)(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szReaderName);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDFORGETREADERGROUPA)(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szGroupName);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDGETCARDTYPEPROVIDERNAMEA)(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szCardName,
        IN SCARDDWORDARG dwProviderId,
        OUT LPTSTR szProvider,
        IN OUT SCARDDWORDARG* pcchProvider);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDGETPROVIDERIDA)(
        IN      SCARDCONTEXT hContext,
        IN      LPCSTR szCard,
        OUT     LPGUID pguidProviderId);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDINTRODUCECARDTYPEA)(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szCardName,
        IN LPCGUID pguidPrimaryProvider,
        IN LPCGUID rgguidInterfaces,
        IN SCARDDWORDARG dwInterfaceCount,
        IN LPCBYTE pbAtr,
        IN LPCBYTE pbAtrMask,
        IN SCARDDWORDARG cbAtrLen);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDINTRODUCEREADERA)(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szReaderName,
        IN LPCSTR szDeviceName);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDINTRODUCEREADERGROUPA)(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szGroupName);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDLISTCARDSA)(
        IN      SCARDCONTEXT hContext,
        IN      LPCBYTE pbAtr,
        IN      LPCGUID rgquidInterfaces,
        IN      SCARDDWORDARG cguidInterfaceCount,
        OUT     LPTSTR mszCards,
        IN OUT  SCARDDWORDARG* pcchCards);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDLISTINTERFACESA)(
        IN      SCARDCONTEXT hContext,
        IN      LPCSTR szCard,
        OUT     LPGUID pguidInterfaces,
        IN OUT  SCARDDWORDARG* pcguidInterfaces);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDLOCATECARDSA)(
        IN      SCARDCONTEXT hContext,
        IN      LPCSTR mszCards,
        IN OUT  LPSCARD_READERSTATEA rgReaderStates,
        IN      SCARDDWORDARG cReaders);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDLOCATECARDSBYATRA)(
        IN      SCARDCONTEXT hContext,
        IN      LPSCARD_ATRMASK rgAtrMasks,
        IN      SCARDDWORDARG cAtrs,
        IN OUT  LPSCARD_READERSTATEA rgReaderStates,
        IN      SCARDDWORDARG cReaders);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDSETCARDTYPEPROVIDERNAMEA)(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szCardName,
        IN SCARDDWORDARG dwProviderId,
        IN LPCSTR szProvider);

    typedef WINSCARDAPI void
    (WINAPI *SCARDRELEASESTARTEDEVENT)(void);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDREMOVEREADERFROMGROUPA)(
        IN SCARDCONTEXT hContext,
        IN LPCTSTR szReaderName,
        IN LPCTSTR szGroupName);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDSTATE)(
        IN SCARDHANDLE hCard,
        OUT SCARDDWORDARG* pdwState,
        OUT SCARDDWORDARG* pdwProtocol,
        OUT LPBYTE pbAtr,
        IN OUT SCARDDWORDARG* pcbAtrLen);

    extern SCARDACCESSSTARTEDEVENT         mySCardAccessStartedEvent;
    extern SCARDADDREADERTOGROUPA          mySCardAddReaderToGroupA;
    extern SCARDFORGETCARDTYPEA            mySCardForgetCardTypeA;
    extern SCARDFORGETREADERA              mySCardForgetReaderA;
    extern SCARDFORGETREADERGROUPA         mySCardForgetReaderGroupA;
    extern SCARDGETCARDTYPEPROVIDERNAMEA   mySCardGetCardTypeProviderNameA;
    extern SCARDGETPROVIDERIDA             mySCardGetProviderIdA;
    extern SCARDINTRODUCECARDTYPEA         mySCardIntroduceCardTypeA;
    extern SCARDINTRODUCEREADERA           mySCardIntroduceReaderA;
    extern SCARDINTRODUCEREADERGROUPA      mySCardIntroduceReaderGroupA;
    extern SCARDLISTCARDSA                 mySCardListCardsA;
    extern SCARDLISTINTERFACESA            mySCardListInterfacesA;
    extern SCARDLOCATECARDSA               mySCardLocateCardsA;
    extern SCARDLOCATECARDSBYATRA          mySCardLocateCardsByATRA;
    extern SCARDRELEASESTARTEDEVENT        mySCardReleaseStartedEvent;
    extern SCARDREMOVEREADERFROMGROUPA     mySCardRemoveReaderFromGroupA;
    extern SCARDSETCARDTYPEPROVIDERNAMEA   mySCardSetCardTypeProviderNameA;
    extern SCARDSTATE                      mySCardState;

#endif // WIN32

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDISVALIDCONTEXT)(
        IN      SCARDCONTEXT hContext);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDGETATTRIB)(
        IN SCARDHANDLE hCard,
        IN SCARDDWORDARG dwAttrId,
        OUT LPBYTE pbAttr,
        IN OUT SCARDDWORDARG* pcbAttrLen);

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDSETATTRIB)(
        IN SCARDHANDLE hCard,
        IN SCARDDWORDARG dwAttrId,
        IN LPCBYTE pbAttr,
        IN SCARDDWORDARG cbAttrLen);

    extern SCARDISVALIDCONTEXT             mySCardIsValidContext;
    extern SCARDGETATTRIB                  mySCardGetAttrib;
    extern SCARDSETATTRIB                  mySCardSetAttrib;

    typedef WINSCARDAPI SCARDRETCODE
    (WINAPI *SCARDCONTROL)(
        IN      SCARDHANDLE hCard,
        IN      SCARDDWORDARG dwControlCode,
        IN      LPCVOID lpInBuffer,
        IN      SCARDDWORDARG nInBufferSize,
        OUT     LPVOID lpOutBuffer,
        IN      SCARDDWORDARG nOutBufferSize,
        OUT     SCARDDWORDARG* lpBytesReturned);



typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDBEGINTRANSACTION)(
    IN      SCARDHANDLE hCard);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDCANCEL)(
    IN      SCARDCONTEXT hContext);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDCANCELTRANSACTION)(
    IN      SCARDHANDLE hCard);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDCONNECTA)(
    IN      SCARDCONTEXT hContext,
    IN      LPCTSTR szReader,
    IN      SCARDDWORDARG dwShareMode,
    IN      SCARDDWORDARG dwPreferredProtocols,
    OUT     LPSCARDHANDLE phCard,
    OUT     SCARDDWORDARG* pdwActiveProtocol);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDDISCONNECT)(
    IN      SCARDHANDLE hCard,
    IN      SCARDDWORDARG dwDisposition);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDENDTRANSACTION)(
    IN      SCARDHANDLE hCard,
    IN      SCARDDWORDARG dwDisposition);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDESTABLISHCONTEXT)(
    IN  SCARDDWORDARG dwScope,
    IN  LPCVOID pvReserved1,
    IN  LPCVOID pvReserved2,
    OUT LPSCARDCONTEXT phContext);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDFREEMEMORY)(
    IN SCARDCONTEXT hContext,
    IN LPCVOID pvMem);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDGETSTATUSCHANGEA)(
    IN      SCARDCONTEXT hContext,
    IN      SCARDDWORDARG dwTimeout,
    IN OUT  LPSCARD_READERSTATEA rgReaderStates,
    IN      SCARDDWORDARG cReaders);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDLISTREADERSA)(
    IN      SCARDCONTEXT hContext,
    IN      LPCTSTR mszGroups,
    OUT     LPTSTR mszReaders,
    IN OUT  SCARDDWORDARG* pcchReaders);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDLISTREADERGROUPSA)(
    IN      SCARDCONTEXT hContext,
    OUT     LPTSTR mszGroups,
    IN OUT  SCARDDWORDARG* pcchGroups);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDRECONNECT)(
    IN      SCARDHANDLE hCard,
    IN      SCARDDWORDARG dwShareMode,
    IN      SCARDDWORDARG dwPreferredProtocols,
    IN      SCARDDWORDARG dwInitialization,
    OUT     SCARDDWORDARG* pdwActiveProtocol);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDRELEASECONTEXT)(
    IN      SCARDCONTEXT hContext);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDSTATUSA)(
    IN SCARDHANDLE hCard,
    OUT LPTSTR szReaderName,
    IN OUT SCARDDWORDARG* pcchReaderLen,
    OUT SCARDDWORDARG* pdwState,
    OUT SCARDDWORDARG* pdwProtocol,
    OUT LPBYTE pbAtr,
    IN OUT SCARDDWORDARG* pcbAtrLen);

typedef WINSCARDAPI SCARDRETCODE
(WINAPI *SCARDTRANSMIT)(
    IN SCARDHANDLE hCard,
    IN LPCSCARD_IO_REQUEST pioSendPci,
    IN LPCBYTE pbSendBuffer,
    IN SCARDDWORDARG cbSendLength,
    IN OUT LPSCARD_IO_REQUEST pioRecvPci,
    OUT LPBYTE pbRecvBuffer,
    IN OUT SCARDDWORDARG* pcbRecvLength);

#ifdef PCSCLITE
typedef WINSCARDAPI char*
(WINAPI *PCSCSTRINGIFYERROR)(
    IN SCARDRETCODE pcscError);

extern PCSCSTRINGIFYERROR              myPcscStringifyError;
#endif // PCSCLITE

extern SCARDBEGINTRANSACTION           mySCardBeginTransaction;
extern SCARDCANCEL                     mySCardCancel;
extern SCARDCONNECTA                   mySCardConnectA;
extern SCARDCONTROL                    mySCardControl;
extern SCARDDISCONNECT                 mySCardDisconnect;
extern SCARDENDTRANSACTION             mySCardEndTransaction;
extern SCARDESTABLISHCONTEXT           mySCardEstablishContext;
extern SCARDFREEMEMORY                 mySCardFreeMemory;
extern SCARDGETSTATUSCHANGEA           mySCardGetStatusChangeA;
extern SCARDLISTREADERSA               mySCardListReadersA;
extern SCARDLISTREADERGROUPSA          mySCardListReaderGroupsA;
extern SCARDRECONNECT                  mySCardReconnect;
extern SCARDRELEASECONTEXT             mySCardReleaseContext;
extern SCARDSTATUSA                    mySCardStatusA;
extern SCARDTRANSMIT                   mySCardTransmit;

extern void * myg_prgSCardT0Pci;
extern void * myg_prgSCardT1Pci;
extern void * myg_prgSCardRawPci;

long winscard_init(void);

#endif // __WINSCARDDLL_H__
