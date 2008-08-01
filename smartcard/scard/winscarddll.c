/*==============================================================================
Copyright 2001-2008 gemalto
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
#ifdef __APPLE__
    #include <stdint.h>
#endif
#include "pcsctypes.h"
#include "winscarddll.h"

#ifdef PCSCLITE
    #include <dlfcn.h>
#endif // PCSCLITE

#ifndef NULL
    #define NULL    ((void*)0)
#endif //NULL

//
// these functions are only available on win32 PCSC
//
#ifdef WIN32
    WINSCARDAPI HANDLE
    WINAPI _defaultSCARDACCESSSTARTEDEVENT(void)
    {
        return NULL;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDADDREADERTOGROUPA(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szReaderName,
        IN LPCSTR szGroupName)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDFORGETCARDTYPEA(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szCardName)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDFORGETREADERA(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szReaderName)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDFORGETREADERGROUPA(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szGroupName)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDGETPROVIDERIDA(
        IN      SCARDCONTEXT hContext,
        IN      LPCSTR szCard,
        OUT     LPGUID pguidProviderId)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDGETCARDTYPEPROVIDERNAMEA(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szCardName,
        IN SCARDDWORDARG dwProviderId,
        OUT LPTSTR szProvider,
        IN OUT SCARDDWORDARG* pcchProvider)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDINTRODUCECARDTYPEA(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szCardName,
        IN LPCGUID pguidPrimaryProvider,
        IN LPCGUID rgguidInterfaces,
        IN SCARDDWORDARG dwInterfaceCount,
        IN LPCBYTE pbAtr,
        IN LPCBYTE pbAtrMask,
        IN SCARDDWORDARG cbAtrLen)
    {
        return SCARD_E_NO_SERVICE;
    }


    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDINTRODUCEREADERA(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szReaderName,
        IN LPCSTR szDeviceName)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDINTRODUCEREADERGROUPA(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szGroupName)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDLISTCARDSA(
        IN      SCARDCONTEXT hContext,
        IN      LPCBYTE pbAtr,
        IN      LPCGUID rgquidInterfaces,
        IN      SCARDDWORDARG cguidInterfaceCount,
        OUT     LPTSTR mszCards,
        IN OUT  SCARDDWORDARG* pcchCards)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDLISTINTERFACESA(
        IN      SCARDCONTEXT hContext,
        IN      LPCSTR szCard,
        OUT     LPGUID pguidInterfaces,
        IN OUT  SCARDDWORDARG* pcguidInterfaces)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDLOCATECARDSA(
        IN      SCARDCONTEXT hContext,
        IN      LPCSTR mszCards,
        IN OUT  LPSCARD_READERSTATEA rgReaderStates,
        IN      SCARDDWORDARG cReaders)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDLOCATECARDSBYATRA(
        IN      SCARDCONTEXT hContext,
        IN      LPSCARD_ATRMASK rgAtrMasks,
        IN      SCARDDWORDARG cAtrs,
        IN OUT  LPSCARD_READERSTATEA rgReaderStates,
        IN      SCARDDWORDARG cReaders)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI void
    WINAPI _defaultSCARDRELEASESTARTEDEVENT(void)
    {
        return;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDREMOVEREADERFROMGROUPA(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szReaderName,
        IN LPCSTR szGroupName)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDSETCARDTYPEPROVIDERNAMEA(
        IN SCARDCONTEXT hContext,
        IN LPCSTR szCardName,
        IN SCARDDWORDARG dwProviderId,
        IN LPCSTR szProvider)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDSTATE(
        IN SCARDHANDLE hCard,
        OUT SCARDDWORDARG* pdwState,
        OUT SCARDDWORDARG* pdwProtocol,
        OUT LPBYTE pbAtr,
        IN OUT SCARDDWORDARG* pcbAtrLen)
    {
        return SCARD_E_NO_SERVICE;
    }

    SCARDACCESSSTARTEDEVENT         mySCardAccessStartedEvent           = _defaultSCARDACCESSSTARTEDEVENT;
    SCARDADDREADERTOGROUPA          mySCardAddReaderToGroupA            = _defaultSCARDADDREADERTOGROUPA;
    SCARDFORGETCARDTYPEA            mySCardForgetCardTypeA              = _defaultSCARDFORGETCARDTYPEA;
    SCARDFORGETREADERA              mySCardForgetReaderA                = _defaultSCARDFORGETREADERA;
    SCARDFORGETREADERGROUPA         mySCardForgetReaderGroupA           = _defaultSCARDFORGETREADERGROUPA;
    SCARDGETPROVIDERIDA             mySCardGetProviderIdA               = _defaultSCARDGETPROVIDERIDA;
    SCARDGETCARDTYPEPROVIDERNAMEA   mySCardGetCardTypeProviderNameA     = _defaultSCARDGETCARDTYPEPROVIDERNAMEA;
    SCARDINTRODUCECARDTYPEA         mySCardIntroduceCardTypeA           = _defaultSCARDINTRODUCECARDTYPEA;
    SCARDINTRODUCEREADERA           mySCardIntroduceReaderA             = _defaultSCARDINTRODUCEREADERA;
    SCARDINTRODUCEREADERGROUPA      mySCardIntroduceReaderGroupA        = _defaultSCARDINTRODUCEREADERGROUPA;
    SCARDLISTCARDSA                 mySCardListCardsA                   = _defaultSCARDLISTCARDSA;
    SCARDLISTINTERFACESA            mySCardListInterfacesA              = _defaultSCARDLISTINTERFACESA;
    SCARDLOCATECARDSA               mySCardLocateCardsA                 = _defaultSCARDLOCATECARDSA;
    SCARDLOCATECARDSBYATRA          mySCardLocateCardsByATRA            = _defaultSCARDLOCATECARDSBYATRA;
    SCARDRELEASESTARTEDEVENT        mySCardReleaseStartedEvent          = _defaultSCARDRELEASESTARTEDEVENT;
    SCARDREMOVEREADERFROMGROUPA     mySCardRemoveReaderFromGroupA       = _defaultSCARDREMOVEREADERFROMGROUPA;
    SCARDSETCARDTYPEPROVIDERNAMEA   mySCardSetCardTypeProviderNameA     = _defaultSCARDSETCARDTYPEPROVIDERNAMEA;
    SCARDSTATE                      mySCardState                        = _defaultSCARDSTATE;
#endif // WIN32

//
// These functions are not available on Max OS X Tiger
//
#ifndef __TIGER__
    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDISVALIDCONTEXT(
        IN      SCARDCONTEXT hContext)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDGETATTRIB(
        IN SCARDHANDLE hCard,
        IN SCARDDWORDARG dwAttrId,
        OUT LPBYTE pbAttr,
        IN OUT SCARDDWORDARG* pcbAttrLen)
    {
        return SCARD_E_NO_SERVICE;
    }

    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDSETATTRIB(
        IN SCARDHANDLE hCard,
        IN SCARDDWORDARG dwAttrId,
        IN LPCBYTE pbAttr,
        IN SCARDDWORDARG cbAttrLen)
    {
        return SCARD_E_NO_SERVICE;
    }

    SCARDISVALIDCONTEXT             mySCardIsValidContext               = _defaultSCARDISVALIDCONTEXT;
    SCARDGETATTRIB                  mySCardGetAttrib                    = _defaultSCARDGETATTRIB;
    SCARDSETATTRIB                  mySCardSetAttrib                    = _defaultSCARDSETATTRIB;

#endif // !__TIGER__

//
// SCardControl does not have the same prototype on Mac OS X Tiger
//
#ifdef __TIGER__
    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDCONTROL(
        IN      SCARDHANDLE hCard,
        IN      const unsigned char* lpInBuffer,
        IN      SCARDDWORDARG nInBufferSize,
        OUT     unsigned char* lpOutBuffer,
        IN OUT  SCARDDWORDARG* lpBytesReturned)
    {
        return SCARD_E_NO_SERVICE;
    }
#else // !__TIGER__
    WINSCARDAPI SCARDRETCODE
    WINAPI _defaultSCARDCONTROL(
        IN      SCARDHANDLE hCard,
        IN      SCARDDWORDARG dwControlCode,
        IN      LPCVOID lpInBuffer,
        IN      SCARDDWORDARG nInBufferSize,
        OUT     LPVOID lpOutBuffer,
        IN      SCARDDWORDARG nOutBufferSize,
        OUT     SCARDDWORDARG* lpBytesReturned)
    {
        return SCARD_E_NO_SERVICE;
    }
#endif // __TIGER__

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDBEGINTRANSACTION(
    IN      SCARDHANDLE hCard)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDCANCEL(
    IN      SCARDCONTEXT hContext)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDCANCELTRANSACTION(
    IN      SCARDHANDLE hCard)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDCONNECTA(
    IN      SCARDCONTEXT hContext,
    IN      LPCTSTR szReader,
    IN      SCARDDWORDARG dwShareMode,
    IN      SCARDDWORDARG dwPreferredProtocols,
    OUT     LPSCARDHANDLE phCard,
    OUT     SCARDDWORDARG* pdwActiveProtocol)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDDISCONNECT(
    IN      SCARDHANDLE hCard,
    IN      SCARDDWORDARG dwDisposition)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDENDTRANSACTION(
    IN      SCARDHANDLE hCard,
    IN      SCARDDWORDARG dwDisposition)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDESTABLISHCONTEXT(
    IN  SCARDDWORDARG dwScope,
    IN  LPCVOID pvReserved1,
    IN  LPCVOID pvReserved2,
    OUT LPSCARDCONTEXT phContext)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDFREEMEMORY(
    IN SCARDCONTEXT hContext,
    IN LPCVOID pvMem)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDGETSTATUSCHANGEA(
    IN      SCARDCONTEXT hContext,
    IN      SCARDDWORDARG dwTimeout,
    IN OUT  LPSCARD_READERSTATEA rgReaderStates,
    IN      SCARDDWORDARG cReaders)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDLISTREADERSA(
    IN      SCARDCONTEXT hContext,
    IN      LPCTSTR mszGroups,
    OUT     LPTSTR mszReaders,
    IN OUT  SCARDDWORDARG* pcchReaders)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDLISTREADERGROUPSA(
    IN      SCARDCONTEXT hContext,
    OUT     LPTSTR mszGroups,
    IN OUT  SCARDDWORDARG* pcchGroups)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDRECONNECT(
    IN      SCARDHANDLE hCard,
    IN      SCARDDWORDARG dwShareMode,
    IN      SCARDDWORDARG dwPreferredProtocols,
    IN      SCARDDWORDARG dwInitialization,
    OUT     SCARDDWORDARG* pdwActiveProtocol)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDRELEASECONTEXT(
    IN      SCARDCONTEXT hContext)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDSTATUSA(
    IN SCARDHANDLE hCard,
    OUT LPTSTR szReaderName,
    IN OUT SCARDDWORDARG* pcchReaderLen,
    OUT SCARDDWORDARG* pdwState,
    OUT SCARDDWORDARG* pdwProtocol,
    OUT LPBYTE pbAtr,
    IN OUT SCARDDWORDARG* pcbAtrLen)
{
    return SCARD_E_NO_SERVICE;
}

WINSCARDAPI SCARDRETCODE
WINAPI _defaultSCARDTRANSMIT(
    IN SCARDHANDLE hCard,
    IN LPCSCARD_IO_REQUEST pioSendPci,
    IN LPCBYTE pbSendBuffer,
    IN SCARDDWORDARG cbSendLength,
    IN OUT LPSCARD_IO_REQUEST pioRecvPci,
    OUT LPBYTE pbRecvBuffer,
    IN OUT SCARDDWORDARG* pcbRecvLength)
{
    return SCARD_E_NO_SERVICE;
}

SCARDBEGINTRANSACTION           mySCardBeginTransaction             = _defaultSCARDBEGINTRANSACTION;
SCARDCANCEL                     mySCardCancel                       = _defaultSCARDCANCEL;
SCARDCANCELTRANSACTION          mySCardCancelTransaction            = _defaultSCARDCANCELTRANSACTION;
SCARDCONNECTA                   mySCardConnectA                     = _defaultSCARDCONNECTA;
SCARDCONTROL                    mySCardControl                      = _defaultSCARDCONTROL;
SCARDDISCONNECT                 mySCardDisconnect                   = _defaultSCARDDISCONNECT;
SCARDENDTRANSACTION             mySCardEndTransaction               = _defaultSCARDENDTRANSACTION;
SCARDESTABLISHCONTEXT           mySCardEstablishContext             = _defaultSCARDESTABLISHCONTEXT;
SCARDFREEMEMORY                 mySCardFreeMemory                   = _defaultSCARDFREEMEMORY;
SCARDGETSTATUSCHANGEA           mySCardGetStatusChangeA             = _defaultSCARDGETSTATUSCHANGEA;
SCARDLISTREADERSA               mySCardListReadersA                 = _defaultSCARDLISTREADERSA;
SCARDLISTREADERGROUPSA          mySCardListReaderGroupsA            = _defaultSCARDLISTREADERGROUPSA;
SCARDRECONNECT                  mySCardReconnect                    = _defaultSCARDRECONNECT;
SCARDRELEASECONTEXT             mySCardReleaseContext               = _defaultSCARDRELEASECONTEXT;
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

        // some functions are not available on older releases of pcsc-lite, such
        // as SCardIsValidContext; don't complain if they are not located
        #define  SILENTGETPROCADDRESS( type, name, realname )  my##name=(type)dlsym( handle, #realname ); \
                                                         dlsym_error = dlerror();

        void* handle=NULL;
        char* dlsym_error;
        char *lib = NULL;
        #ifdef __APPLE__
            lib = "/System/Library/Frameworks/PCSC.framework/PCSC";
        #else
            lib = "libpcsclite.so";
        #endif

        if( bFirstCall )
        {
            bFirstCall=FALSE;
            dlerror();
            handle = dlopen( lib, RTLD_NOW );
            if( NULL!=handle )
            {
                lRetCode=SCARD_S_SUCCESS;
                GETPROCADDRESS( SCARDBEGINTRANSACTION  , SCardBeginTransaction  , SCardBeginTransaction  );
                GETPROCADDRESS( SCARDCANCEL            , SCardCancel            , SCardCancel );
                GETPROCADDRESS( SCARDCANCELTRANSACTION , SCardCancelTransaction , SCardCancelTransaction );
                GETPROCADDRESS( SCARDCONNECTA          , SCardConnectA          , SCardConnect           );
                GETPROCADDRESS( SCARDDISCONNECT        , SCardDisconnect        , SCardDisconnect        );
                GETPROCADDRESS( SCARDENDTRANSACTION    , SCardEndTransaction    , SCardEndTransaction    );
                GETPROCADDRESS( SCARDESTABLISHCONTEXT  , SCardEstablishContext  , SCardEstablishContext  );
                GETPROCADDRESS( SCARDGETSTATUSCHANGEA  , SCardGetStatusChangeA  , SCardGetStatusChange   );
                GETPROCADDRESS( SCARDLISTREADERSA      , SCardListReadersA      , SCardListReaders       );
                GETPROCADDRESS( SCARDLISTREADERGROUPSA , SCardListReaderGroupsA , SCardListReaderGroups  );
                GETPROCADDRESS( SCARDRECONNECT         , SCardReconnect         , SCardReconnect         );
                GETPROCADDRESS( SCARDRELEASECONTEXT    , SCardReleaseContext    , SCardReleaseContext    );
                GETPROCADDRESS( SCARDSTATUSA           , SCardStatusA           , SCardStatus            );
                GETPROCADDRESS( SCARDTRANSMIT          , SCardTransmit          , SCardTransmit          );

                #ifndef __APPLE__
                    GETPROCADDRESS( SCARDCONTROL, SCardControl, SCardControl );
                #else // !__APPLE__
                    #ifdef __TIGER__
                        GETPROCADDRESS( SCARDCONTROL, SCardControl, SCardControl );
                    #else // ! __TIGER__
                        GETPROCADDRESS( SCARDCONTROL, SCardControl, SCardControl132 );
                    #endif // __TIGER__
                #endif // __APPLE__

                #ifndef __TIGER__
                    SILENTGETPROCADDRESS( SCARDISVALIDCONTEXT    , SCardIsValidContext    , SCardIsValidContext    );
                    GETPROCADDRESS( SCARDGETATTRIB         , SCardGetAttrib         , SCardGetAttrib         );
                    GETPROCADDRESS( SCARDSETATTRIB         , SCardSetAttrib         , SCardSetAttrib         );
                #endif

                myg_prgSCardT0Pci   = (unsigned long)dlsym( handle, "g_rgSCardT0Pci"  );
                myg_prgSCardT1Pci   = (unsigned long)dlsym( handle, "g_rgSCardT1Pci"  );
                myg_prgSCardRawPci  = (unsigned long)dlsym( handle, "g_rgSCardRawPci" );

                dlclose( handle );
                dlsym_error = dlerror();
                if( NULL!= dlsym_error )
                {
                    printf( "Failed to load symbol address from %s: %s!", lib, (char*)dlsym_error );
                }
            }
            else
            {
                dlsym_error = dlerror();
                if( NULL!= dlsym_error )
                {
                    printf( "Failed to dlopen %s: %s!", lib, (dlsym_error==NULL) ? "" : (char*)dlsym_error );
                }
            }
         }
    #endif // PCSCLITE
    return lRetCode;
};

