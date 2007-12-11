/*==============================================================================
Copyright 2001-2007 gemalto
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
#ifdef WIN32
    #include <windows.h>
#endif

#ifdef __APPLE__
    #ifndef PCSC_API
        #define PCSC_API
    #endif
    #include <PCSC/wintypes.h>
    #include <PCSC/winscard.h>
    #define LPCTSTR char*
#else //__APPLE__
#include <winscard.h>
#endif 

#ifdef PCSCLITE
    #define WINSCARDAPI PCSC_API
    #define WINAPI
    #define IN
    #define OUT
    #define LPSCARD_READERSTATEA LPSCARD_READERSTATE_A
    #define SCARD_AUTOALLOCATE (DWORD)(-1)
    #ifndef FALSE
        #define FALSE (0==1)
    #endif // FALSE
    #ifndef TRUE
        #define TRUE (1==1)
    #endif
#endif // PCSCLITE

#ifdef WIN32
typedef WINSCARDAPI HANDLE
(WINAPI *SCARDACCESSSTARTEDEVENT)(void);

typedef WINSCARDAPI LONG
(WINAPI *SCARDADDREADERTOGROUPA)(
    IN SCARDCONTEXT hContext,
    IN LPCTSTR szReaderName,
    IN LPCTSTR szGroupName);

typedef WINSCARDAPI LONG
(WINAPI *SCARDFORGETCARDTYPEA)(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szCardName);

typedef WINSCARDAPI LONG
(WINAPI *SCARDFORGETREADERA)(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szReaderName);


typedef WINSCARDAPI LONG
(WINAPI *SCARDFORGETREADERGROUPA)(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szGroupName);

typedef WINSCARDAPI LONG
(WINAPI *SCARDGETCARDTYPEPROVIDERNAMEA)(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szCardName,
    IN DWORD dwProviderId,
    OUT LPTSTR szProvider,
    IN OUT LPDWORD pcchProvider);

typedef WINSCARDAPI LONG
(WINAPI *SCARDGETPROVIDERIDA)(
    IN      SCARDCONTEXT hContext,
    IN      LPCSTR szCard,
    OUT     LPGUID pguidProviderId);

typedef WINSCARDAPI LONG
(WINAPI *SCARDINTRODUCECARDTYPEA)(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szCardName,
    IN LPCGUID pguidPrimaryProvider,
    IN LPCGUID rgguidInterfaces,
    IN DWORD dwInterfaceCount,
    IN LPCBYTE pbAtr,
    IN LPCBYTE pbAtrMask,
    IN DWORD cbAtrLen);

typedef WINSCARDAPI LONG
(WINAPI *SCARDINTRODUCEREADERA)(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szReaderName,
    IN LPCSTR szDeviceName);

typedef WINSCARDAPI LONG
(WINAPI *SCARDINTRODUCEREADERGROUPA)(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szGroupName);

typedef WINSCARDAPI LONG
(WINAPI *SCARDLISTCARDSA)(
    IN      SCARDCONTEXT hContext,
    IN      LPCBYTE pbAtr,
    IN      LPCGUID rgquidInterfaces,
    IN      DWORD cguidInterfaceCount,
    OUT     LPTSTR mszCards,
    IN OUT  LPDWORD pcchCards);

typedef WINSCARDAPI LONG
(WINAPI *SCARDLISTINTERFACESA)(
    IN      SCARDCONTEXT hContext,
    IN      LPCSTR szCard,
    OUT     LPGUID pguidInterfaces,
    IN OUT  LPDWORD pcguidInterfaces);

typedef WINSCARDAPI LONG
(WINAPI *SCARDLOCATECARDSA)(
    IN      SCARDCONTEXT hContext,
    IN      LPCSTR mszCards,
    IN OUT  LPSCARD_READERSTATEA rgReaderStates,
    IN      DWORD cReaders);

typedef WINSCARDAPI LONG
(WINAPI *SCARDLOCATECARDSBYATRA)(
    IN      SCARDCONTEXT hContext,
    IN      LPSCARD_ATRMASK rgAtrMasks,
    IN      DWORD cAtrs,
    IN OUT  LPSCARD_READERSTATEA rgReaderStates,
    IN      DWORD cReaders);

typedef WINSCARDAPI LONG
(WINAPI *SCARDSETCARDTYPEPROVIDERNAMEA)(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szCardName,
    IN DWORD dwProviderId,
    IN LPCSTR szProvider);

typedef WINSCARDAPI LONG
(WINAPI *SCARDSTATE)(
    IN SCARDHANDLE hCard,
    OUT LPDWORD pdwState,
    OUT LPDWORD pdwProtocol,
    OUT LPBYTE pbAtr,
    IN OUT LPDWORD pcbAtrLen);
#endif // WIN32

typedef WINSCARDAPI LONG
(WINAPI *SCARDBEGINTRANSACTION)(
    IN      SCARDHANDLE hCard);

typedef WINSCARDAPI LONG
(WINAPI *SCARDCANCEL)(
    IN      SCARDCONTEXT hContext);

typedef WINSCARDAPI LONG
(WINAPI *SCARDCANCELTRANSACTION)(
    IN      SCARDHANDLE hCard);

typedef WINSCARDAPI LONG
(WINAPI *SCARDCONNECTA)(
    IN      SCARDCONTEXT hContext,
    IN      LPCTSTR szReader,
    IN      DWORD dwShareMode,
    IN      DWORD dwPreferredProtocols,
    OUT     LPSCARDHANDLE phCard,
    OUT     LPDWORD pdwActiveProtocol);

typedef WINSCARDAPI LONG
(WINAPI *SCARDCONTROL)(
    IN      SCARDHANDLE hCard,
    IN      DWORD dwControlCode,
    IN      LPCVOID lpInBuffer,
    IN      DWORD nInBufferSize,
    OUT     LPVOID lpOutBuffer,
    IN      DWORD nOutBufferSize,
    OUT     LPDWORD lpBytesReturned);


typedef WINSCARDAPI LONG
(WINAPI *SCARDDISCONNECT)(
    IN      SCARDHANDLE hCard,
    IN      DWORD dwDisposition);

typedef WINSCARDAPI LONG
(WINAPI *SCARDENDTRANSACTION)(
    IN      SCARDHANDLE hCard,
    IN      DWORD dwDisposition);

typedef WINSCARDAPI LONG
(WINAPI *SCARDESTABLISHCONTEXT)(
    IN  DWORD dwScope,
    IN  LPCVOID pvReserved1,
    IN  LPCVOID pvReserved2,
    OUT unsigned long* phContext);

typedef WINSCARDAPI LONG
(WINAPI *SCARDFREEMEMORY)(
    IN SCARDCONTEXT hContext,
    IN LPCVOID pvMem);

typedef WINSCARDAPI LONG
(WINAPI *SCARDGETATTRIB)(
    IN SCARDHANDLE hCard,
    IN DWORD dwAttrId,
    OUT LPBYTE pbAttr,
    IN OUT LPDWORD pcbAttrLen);

typedef WINSCARDAPI LONG
(WINAPI *SCARDGETSTATUSCHANGEA)(
    IN      SCARDCONTEXT hContext,
    IN      DWORD dwTimeout,
    IN OUT  LPSCARD_READERSTATEA rgReaderStates,
    IN      DWORD cReaders);

typedef WINSCARDAPI LONG
(WINAPI *SCARDISVALIDCONTEXT)(
    IN      SCARDCONTEXT hContext);

typedef WINSCARDAPI LONG
(WINAPI *SCARDLISTREADERSA)(
    IN      SCARDCONTEXT hContext,
    IN      LPCTSTR mszGroups,
    OUT     LPTSTR mszReaders,
    IN OUT  LPDWORD pcchReaders);

typedef WINSCARDAPI LONG
(WINAPI *SCARDLISTREADERGROUPSA)(
    IN      SCARDCONTEXT hContext,
    OUT     LPTSTR mszGroups,
    IN OUT  LPDWORD pcchGroups);

typedef WINSCARDAPI LONG
(WINAPI *SCARDRECONNECT)(
    IN      SCARDHANDLE hCard,
    IN      DWORD dwShareMode,
    IN      DWORD dwPreferredProtocols,
    IN      DWORD dwInitialization,
    OUT     LPDWORD pdwActiveProtocol);

typedef WINSCARDAPI LONG
(WINAPI *SCARDRELEASECONTEXT)(
    IN      SCARDCONTEXT hContext);

typedef WINSCARDAPI void
(WINAPI *SCARDRELEASESTARTEDEVENT)(void);

typedef WINSCARDAPI LONG
(WINAPI *SCARDREMOVEREADERFROMGROUPA)(
    IN SCARDCONTEXT hContext,
    IN LPCTSTR szReaderName,
    IN LPCTSTR szGroupName);

typedef WINSCARDAPI LONG
(WINAPI *SCARDSETATTRIB)(
    IN SCARDHANDLE hCard,
    IN DWORD dwAttrId,
    IN LPCBYTE pbAttr,
    IN DWORD cbAttrLen);

typedef WINSCARDAPI LONG
(WINAPI *SCARDSTATUSA)(
    IN SCARDHANDLE hCard,
    OUT LPTSTR szReaderName,
    IN OUT LPDWORD pcchReaderLen,
    OUT LPDWORD pdwState,
    OUT LPDWORD pdwProtocol,
    OUT LPBYTE pbAtr,
    IN OUT LPDWORD pcbAtrLen);


typedef WINSCARDAPI LONG
(WINAPI *SCARDTRANSMIT)(
    IN SCARDHANDLE hCard,
    IN LPCSCARD_IO_REQUEST pioSendPci,
    IN LPCBYTE pbSendBuffer,
    IN DWORD cbSendLength,
    IN OUT LPSCARD_IO_REQUEST pioRecvPci,
    OUT LPBYTE pbRecvBuffer,
    IN OUT LPDWORD pcbRecvLength);

// these functions are not supported by pcsc-lite
#ifdef WIN32
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

extern SCARDBEGINTRANSACTION           mySCardBeginTransaction;
extern SCARDCANCEL                     mySCardCancel;
extern SCARDCANCELTRANSACTION          mySCardCancelTransaction;
extern SCARDCONNECTA                   mySCardConnectA;
extern SCARDCONTROL                    mySCardControl;
extern SCARDDISCONNECT                 mySCardDisconnect;
extern SCARDENDTRANSACTION             mySCardEndTransaction;
extern SCARDESTABLISHCONTEXT           mySCardEstablishContext;
extern SCARDFREEMEMORY                 mySCardFreeMemory;
extern SCARDGETATTRIB                  mySCardGetAttrib;
extern SCARDGETSTATUSCHANGEA           mySCardGetStatusChangeA;
extern SCARDISVALIDCONTEXT             mySCardIsValidContext;
extern SCARDLISTREADERSA               mySCardListReadersA;
extern SCARDLISTREADERGROUPSA          mySCardListReaderGroupsA;
extern SCARDRECONNECT                  mySCardReconnect;
extern SCARDRELEASECONTEXT             mySCardReleaseContext;
extern SCARDSETATTRIB                  mySCardSetAttrib;
extern SCARDSTATUSA                    mySCardStatusA;
extern SCARDTRANSMIT                   mySCardTransmit;


extern unsigned long myg_prgSCardT0Pci;
extern unsigned long myg_prgSCardT1Pci;
extern unsigned long myg_prgSCardRawPci;

long winscard_init(void);
