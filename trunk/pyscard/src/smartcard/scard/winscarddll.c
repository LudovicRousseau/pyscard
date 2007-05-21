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
#include <stdio.h>

#include "winscarddll.h"

#ifdef PCSCLITE
#include <dlfcn.h>
#endif // PCSCLITE

#ifndef NULL
#define NULL    ((void*)0)
#endif //NULL

// isolate functions not supported by pcsc lite
#ifdef WIN32
WINSCARDAPI HANDLE
WINAPI _defaultSCARDACCESSSTARTEDEVENT(void)
{
    return NULL;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDADDREADERTOGROUPA(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szReaderName,
    IN LPCSTR szGroupName)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDCANCEL(
    IN      SCARDCONTEXT hContext)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDCONTROL(
    IN      SCARDHANDLE hCard,
    IN      DWORD dwControlCode,
    IN      LPCVOID lpInBuffer,
    IN      DWORD nInBufferSize,
    OUT     LPVOID lpOutBuffer,
    IN      DWORD nOutBufferSize,
    OUT     LPDWORD lpBytesReturned)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDFORGETCARDTYPEA(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szCardName)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDFORGETREADERA(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szReaderName)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDFORGETREADERGROUPA(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szGroupName)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDGETPROVIDERIDA(
    IN      SCARDCONTEXT hContext,
    IN      LPCSTR szCard,
    OUT     LPGUID pguidProviderId)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDGETCARDTYPEPROVIDERNAMEA(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szCardName,
    IN DWORD dwProviderId,
    OUT LPTSTR szProvider,
    IN OUT LPDWORD pcchProvider)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDINTRODUCECARDTYPEA(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szCardName,
    IN LPCGUID pguidPrimaryProvider,
    IN LPCGUID rgguidInterfaces,
    IN DWORD dwInterfaceCount,
    IN LPCBYTE pbAtr,
    IN LPCBYTE pbAtrMask,
    IN DWORD cbAtrLen)
{
    return SCARD_E_NO_SERVICE;
}


WINSCARDAPI LONG
WINAPI _defaultSCARDINTRODUCEREADERA(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szReaderName,
    IN LPCSTR szDeviceName)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDINTRODUCEREADERGROUPA(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szGroupName)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDISVALIDCONTEXT(
    IN      SCARDCONTEXT hContext)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDLISTCARDSA(
    IN      SCARDCONTEXT hContext,
    IN      LPCBYTE pbAtr,
    IN      LPCGUID rgquidInterfaces,
    IN      DWORD cguidInterfaceCount,
    OUT     LPTSTR mszCards,
    IN OUT  LPDWORD pcchCards)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDLISTINTERFACESA(
    IN      SCARDCONTEXT hContext,
    IN      LPCSTR szCard,
    OUT     LPGUID pguidInterfaces,
    IN OUT  LPDWORD pcguidInterfaces)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDLOCATECARDSA(
    IN      SCARDCONTEXT hContext,
    IN      LPCSTR mszCards,
    IN OUT  LPSCARD_READERSTATEA rgReaderStates,
    IN      DWORD cReaders)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDLOCATECARDSBYATRA(
    IN      SCARDCONTEXT hContext,
    IN      LPSCARD_ATRMASK rgAtrMasks,
    IN      DWORD cAtrs,
    IN OUT  LPSCARD_READERSTATEA rgReaderStates,
    IN      DWORD cReaders)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI void
WINAPI _defaultSCARDRELEASESTARTEDEVENT(void)
{
    return;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDREMOVEREADERFROMGROUPA(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szReaderName,
    IN LPCSTR szGroupName)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDSETCARDTYPEPROVIDERNAMEA(
    IN SCARDCONTEXT hContext,
    IN LPCSTR szCardName,
    IN DWORD dwProviderId,
    IN LPCSTR szProvider)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDSTATE(
    IN SCARDHANDLE hCard,
    OUT LPDWORD pdwState,
    OUT LPDWORD pdwProtocol,
    OUT LPBYTE pbAtr,
    IN OUT LPDWORD pcbAtrLen)
{
    return SCARD_E_NO_SERVICE;
}

#endif // WIN32

WINSCARDAPI LONG
WINAPI _defaultSCARDBEGINTRANSACTION(
    IN      SCARDHANDLE hCard)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDCANCELTRANSACTION(
    IN      SCARDHANDLE hCard)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDCONNECTA(
    IN      SCARDCONTEXT hContext,
    IN      _LPCSTR szReader,
    IN      DWORD dwShareMode,
    IN      DWORD dwPreferredProtocols,
    OUT     LPSCARDHANDLE phCard,
    OUT     LPDWORD pdwActiveProtocol)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDDISCONNECT(
    IN      SCARDHANDLE hCard,
    IN      DWORD dwDisposition)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDENDTRANSACTION(
    IN      SCARDHANDLE hCard,
    IN      DWORD dwDisposition)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDESTABLISHCONTEXT(
    IN  DWORD dwScope,
    IN  LPCVOID pvReserved1,
    IN  LPCVOID pvReserved2,
    OUT LPSCARDCONTEXT phContext)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDFREEMEMORY(
    IN SCARDCONTEXT hContext,
    IN LPCVOID pvMem)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDGETATTRIB(
    IN SCARDHANDLE hCard,
    IN DWORD dwAttrId,
    OUT LPBYTE pbAttr,
    IN OUT LPDWORD pcbAttrLen)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDGETSTATUSCHANGEA(
    IN      SCARDCONTEXT hContext,
    IN      DWORD dwTimeout,
    IN OUT  LPSCARD_READERSTATEA rgReaderStates,
    IN      DWORD cReaders)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDLISTREADERSA(
    IN      SCARDCONTEXT hContext,
    IN      LPCTSTR mszGroups,
    OUT     LPTSTR mszReaders,
    IN OUT  LPDWORD pcchReaders)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDLISTREADERGROUPSA(
    IN      SCARDCONTEXT hContext,
    OUT     LPTSTR mszGroups,
    IN OUT  LPDWORD pcchGroups)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDRECONNECT(
    IN      SCARDHANDLE hCard,
    IN      DWORD dwShareMode,
    IN      DWORD dwPreferredProtocols,
    IN      DWORD dwInitialization,
    OUT     LPDWORD pdwActiveProtocol)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDRELEASECONTEXT(
    IN      SCARDCONTEXT hContext)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDSETATTRIB(
    IN SCARDHANDLE hCard,
    IN DWORD dwAttrId,
    IN LPCBYTE pbAttr,
    IN DWORD cbAttrLen)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDSTATUSA(
    IN SCARDHANDLE hCard,
    OUT LPTSTR szReaderName,
    IN OUT LPDWORD pcchReaderLen,
    OUT LPDWORD pdwState,
    OUT LPDWORD pdwProtocol,
    OUT LPBYTE pbAtr,
    IN OUT LPDWORD pcbAtrLen)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI LONG
WINAPI _defaultSCARDTRANSMIT(
    IN SCARDHANDLE hCard,
    IN LPCSCARD_IO_REQUEST pioSendPci,
    IN LPCBYTE pbSendBuffer,
    IN DWORD cbSendLength,
    IN OUT LPSCARD_IO_REQUEST pioRecvPci,
    OUT LPBYTE pbRecvBuffer,
    IN OUT LPDWORD pcbRecvLength)
{
    return SCARD_E_NO_SERVICE;
}

#ifdef WIN32
SCARDACCESSSTARTEDEVENT         mySCardAccessStartedEvent           = _defaultSCARDACCESSSTARTEDEVENT;
SCARDADDREADERTOGROUPA          mySCardAddReaderToGroupA            = _defaultSCARDADDREADERTOGROUPA;
SCARDCANCEL                     mySCardCancel                       = _defaultSCARDCANCEL;
SCARDCONTROL                    mySCardControl                      = _defaultSCARDCONTROL;
SCARDFORGETCARDTYPEA            mySCardForgetCardTypeA              = _defaultSCARDFORGETCARDTYPEA;
SCARDFORGETREADERA              mySCardForgetReaderA                = _defaultSCARDFORGETREADERA;
SCARDFORGETREADERGROUPA         mySCardForgetReaderGroupA           = _defaultSCARDFORGETREADERGROUPA;
SCARDGETPROVIDERIDA             mySCardGetProviderIdA               = _defaultSCARDGETPROVIDERIDA;
SCARDGETCARDTYPEPROVIDERNAMEA   mySCardGetCardTypeProviderNameA     = _defaultSCARDGETCARDTYPEPROVIDERNAMEA;
SCARDINTRODUCECARDTYPEA         mySCardIntroduceCardTypeA           = _defaultSCARDINTRODUCECARDTYPEA;
SCARDINTRODUCEREADERA           mySCardIntroduceReaderA             = _defaultSCARDINTRODUCEREADERA;
SCARDINTRODUCEREADERGROUPA      mySCardIntroduceReaderGroupA        = _defaultSCARDINTRODUCEREADERGROUPA;
SCARDISVALIDCONTEXT             mySCardIsValidContext               = _defaultSCARDISVALIDCONTEXT;
SCARDLISTCARDSA                 mySCardListCardsA                   = _defaultSCARDLISTCARDSA;
SCARDLISTINTERFACESA            mySCardListInterfacesA              = _defaultSCARDLISTINTERFACESA;
SCARDLOCATECARDSA               mySCardLocateCardsA                 = _defaultSCARDLOCATECARDSA;
SCARDLOCATECARDSBYATRA          mySCardLocateCardsByATRA            = _defaultSCARDLOCATECARDSBYATRA;
SCARDRELEASESTARTEDEVENT        mySCardReleaseStartedEvent          = _defaultSCARDRELEASESTARTEDEVENT;
SCARDREMOVEREADERFROMGROUPA     mySCardRemoveReaderFromGroupA       = _defaultSCARDREMOVEREADERFROMGROUPA;
SCARDSETCARDTYPEPROVIDERNAMEA   mySCardSetCardTypeProviderNameA     = _defaultSCARDSETCARDTYPEPROVIDERNAMEA;
SCARDSTATE                      mySCardState                        = _defaultSCARDSTATE;
#endif // WIN32

SCARDBEGINTRANSACTION           mySCardBeginTransaction             = _defaultSCARDBEGINTRANSACTION;
SCARDCANCELTRANSACTION          mySCardCancelTransaction            = _defaultSCARDCANCELTRANSACTION;
SCARDCONNECTA                   mySCardConnectA                     = _defaultSCARDCONNECTA;
SCARDDISCONNECT                 mySCardDisconnect                   = _defaultSCARDDISCONNECT;
SCARDENDTRANSACTION             mySCardEndTransaction               = _defaultSCARDENDTRANSACTION;
SCARDESTABLISHCONTEXT           mySCardEstablishContext             = _defaultSCARDESTABLISHCONTEXT;
SCARDFREEMEMORY                 mySCardFreeMemory                   = _defaultSCARDFREEMEMORY;
SCARDGETATTRIB                  mySCardGetAttrib                    = _defaultSCARDGETATTRIB;
SCARDGETSTATUSCHANGEA           mySCardGetStatusChangeA             = _defaultSCARDGETSTATUSCHANGEA;
SCARDLISTREADERSA               mySCardListReadersA                 = _defaultSCARDLISTREADERSA;
SCARDLISTREADERGROUPSA          mySCardListReaderGroupsA            = _defaultSCARDLISTREADERGROUPSA;
SCARDRECONNECT                  mySCardReconnect                    = _defaultSCARDRECONNECT;
SCARDRELEASECONTEXT             mySCardReleaseContext               = _defaultSCARDRELEASECONTEXT;
SCARDSETATTRIB                  mySCardSetAttrib                    = _defaultSCARDSETATTRIB;
SCARDSTATUSA                    mySCardStatusA                      = _defaultSCARDSTATUSA;
SCARDTRANSMIT                   mySCardTransmit                     = _defaultSCARDTRANSMIT;



unsigned long myg_prgSCardT0Pci=0L;
unsigned long myg_prgSCardT1Pci=0L;
unsigned long myg_prgSCardRawPci=0L;


long winscard_init(void)
{
    static BOOL bFirstCall=TRUE;
    static long lRetCode=SCARD_E_NO_SERVICE;
    #ifdef WIN32
        #define  GETPROCADDRESS(type,name)       my##name=(type)GetProcAddress(hinstDLL, #name );
        HINSTANCE hinstDLL=NULL;
    
        if( bFirstCall )
        {
            bFirstCall=FALSE;
            hinstDLL = LoadLibrary( "winscard.dll" );
            if( NULL!=hinstDLL )
            {
                lRetCode=SCARD_S_SUCCESS;
                GETPROCADDRESS( SCARDADDREADERTOGROUPA          , SCardAddReaderToGroupA );
                GETPROCADDRESS( SCARDACCESSSTARTEDEVENT         , SCardAccessStartedEvent );
                GETPROCADDRESS( SCARDBEGINTRANSACTION           , SCardBeginTransaction );
                GETPROCADDRESS( SCARDCANCEL                     , SCardCancel );
                GETPROCADDRESS( SCARDCANCELTRANSACTION          , SCardCancelTransaction );
                GETPROCADDRESS( SCARDCONNECTA                   , SCardConnectA );
                GETPROCADDRESS( SCARDCONTROL                    , SCardControl );
                GETPROCADDRESS( SCARDDISCONNECT                 , SCardDisconnect );
                GETPROCADDRESS( SCARDENDTRANSACTION             , SCardEndTransaction );
                GETPROCADDRESS( SCARDESTABLISHCONTEXT           , SCardEstablishContext );
                GETPROCADDRESS( SCARDFORGETCARDTYPEA            , SCardForgetCardTypeA );
                GETPROCADDRESS( SCARDFORGETREADERA              , SCardForgetReaderA );
                GETPROCADDRESS( SCARDFORGETREADERGROUPA         , SCardForgetReaderGroupA );
                GETPROCADDRESS( SCARDFREEMEMORY                 , SCardFreeMemory );
                GETPROCADDRESS( SCARDGETCARDTYPEPROVIDERNAMEA   , SCardGetCardTypeProviderNameA );
                GETPROCADDRESS( SCARDGETATTRIB                  , SCardGetAttrib );
                GETPROCADDRESS( SCARDGETPROVIDERIDA             , SCardGetProviderIdA );
                GETPROCADDRESS( SCARDGETSTATUSCHANGEA           , SCardGetStatusChangeA );
                GETPROCADDRESS( SCARDINTRODUCECARDTYPEA         , SCardIntroduceCardTypeA );
                GETPROCADDRESS( SCARDINTRODUCEREADERA           , SCardIntroduceReaderA );
                GETPROCADDRESS( SCARDINTRODUCEREADERGROUPA      , SCardIntroduceReaderGroupA );
                GETPROCADDRESS( SCARDISVALIDCONTEXT             , SCardIsValidContext );
                GETPROCADDRESS( SCARDLISTCARDSA                 , SCardListCardsA );
                GETPROCADDRESS( SCARDLISTINTERFACESA            , SCardListInterfacesA );
                GETPROCADDRESS( SCARDLISTREADERSA               , SCardListReadersA );
                GETPROCADDRESS( SCARDLISTREADERGROUPSA          , SCardListReaderGroupsA );
                GETPROCADDRESS( SCARDLOCATECARDSA               , SCardLocateCardsA );
                GETPROCADDRESS( SCARDLOCATECARDSBYATRA          , SCardLocateCardsByATRA );
                GETPROCADDRESS( SCARDRECONNECT                  , SCardReconnect );
                GETPROCADDRESS( SCARDRELEASECONTEXT             , SCardReleaseContext );
                GETPROCADDRESS( SCARDRELEASESTARTEDEVENT        , SCardReleaseStartedEvent );
                GETPROCADDRESS( SCARDREMOVEREADERFROMGROUPA     , SCardRemoveReaderFromGroupA );
                GETPROCADDRESS( SCARDSETATTRIB                  , SCardSetAttrib );
                GETPROCADDRESS( SCARDSETCARDTYPEPROVIDERNAMEA   , SCardSetCardTypeProviderNameA );
                GETPROCADDRESS( SCARDSTATE                      , SCardState );
                GETPROCADDRESS( SCARDSTATUSA                    , SCardStatusA );
                GETPROCADDRESS( SCARDTRANSMIT                   , SCardTransmit );
    
    
                myg_prgSCardT0Pci   = (unsigned long)GetProcAddress( hinstDLL, "g_rgSCardT0Pci"  );
                myg_prgSCardT1Pci   = (unsigned long)GetProcAddress( hinstDLL, "g_rgSCardT1Pci"  );
                myg_prgSCardRawPci  = (unsigned long)GetProcAddress( hinstDLL, "g_rgSCardRawPci" );
    
            }
         }
    #endif // WIN32
    #ifdef PCSCLITE
        #define  GETPROCADDRESS( type, name, realname )  my##name=(type)dlsym( handle, #realname ); \
                                                         dlsym_error = dlerror(); \
                                                         if (NULL!=dlsym_error) \
                                                         { \
                                                            printf( "Failed to load symbol for: %s, %s!\n", #realname, (char*)dlsym_error ); \
                                                         }
        void* handle=NULL;
        char* dlsym_error;

        if( bFirstCall )
        {
            bFirstCall=FALSE;
            dlerror();
            handle = dlopen( "libpcsclite.so", RTLD_NOW );
            if( NULL!=handle )
            {
                lRetCode=SCARD_S_SUCCESS;
                GETPROCADDRESS( SCARDBEGINTRANSACTION  , SCardBeginTransaction  , SCardBeginTransaction  );
                GETPROCADDRESS( SCARDCANCELTRANSACTION , SCardCancelTransaction , SCardCancelTransaction );
                GETPROCADDRESS( SCARDCONNECTA          , SCardConnectA          , SCardConnect           );
                GETPROCADDRESS( SCARDDISCONNECT        , SCardDisconnect        , SCardDisconnect        );
                GETPROCADDRESS( SCARDENDTRANSACTION    , SCardEndTransaction    , SCardEndTransaction    );
                GETPROCADDRESS( SCARDESTABLISHCONTEXT  , SCardEstablishContext  , SCardEstablishContext  );
                GETPROCADDRESS( SCARDGETATTRIB         , SCardGetAttrib         , SCardGetAttrib         );
                GETPROCADDRESS( SCARDGETSTATUSCHANGEA  , SCardGetStatusChangeA  , SCardGetStatusChange   );
                GETPROCADDRESS( SCARDLISTREADERSA      , SCardListReadersA      , SCardListReaders       );
                GETPROCADDRESS( SCARDLISTREADERGROUPSA , SCardListReaderGroupsA , SCardListReaderGroups  );
                GETPROCADDRESS( SCARDRECONNECT         , SCardReconnect         , SCardReconnect         );
                GETPROCADDRESS( SCARDRELEASECONTEXT    , SCardReleaseContext    , SCardReleaseContext    );
                GETPROCADDRESS( SCARDSETATTRIB         , SCardSetAttrib         , SCardSetAttrib         );
                GETPROCADDRESS( SCARDSTATUSA           , SCardStatusA           , SCardStatus            );
                GETPROCADDRESS( SCARDTRANSMIT          , SCardTransmit          , SCardTransmit          );

                
                myg_prgSCardT0Pci   = (unsigned long)dlsym( handle, "g_rgSCardT0Pci"  );
                myg_prgSCardT1Pci   = (unsigned long)dlsym( handle, "g_rgSCardT1Pci"  );
                myg_prgSCardRawPci  = (unsigned long)dlsym( handle, "g_rgSCardRawPci" );

                dlclose( handle );
                dlsym_error = dlerror();
                if( NULL!= dlsym_error )
                {
                    printf( "Failed to load symbol address from libpcsclite.so: %s!", (char*)dlsym_error ); 
                }
            }
            else
            {
                dlsym_error = dlerror();
                if( NULL!= dlsym_error )
                {
                    printf( "Failed to dlopen libpcsclite.so: %s!", (dlsym_error==NULL) ? "" : (char*)dlsym_error ); 
                }
            }
         }
    #endif // PCSCLITE
    return lRetCode;
};




