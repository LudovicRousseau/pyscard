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

typedef enum
{
    SCARD_SCOPE_USER,
    SCARD_SCOPE_TERMINAL,
    SCARD_SCOPE_SYSTEM
}  ScopeType ;

typedef enum
{
    SCARD_SHARE_SHARED,
    SCARD_SHARE_EXCLUSIVE,
    SCARD_SHARE_DIRECT
}  ShareType ;

typedef enum
{
    SCARD_LEAVE_CARD,
    SCARD_RESET_CARD,
    SCARD_UNPOWER_CARD,
    SCARD_EJECT_CARD
} DispositionType ;

typedef enum
{
    SCARD_STATE_UNAWARE,
    SCARD_STATE_IGNORE,
    SCARD_STATE_CHANGED,
    SCARD_STATE_UNKNOWN,
    SCARD_STATE_UNAVAILABLE,
    SCARD_STATE_EMPTY,
    SCARD_STATE_PRESENT,
    SCARD_STATE_ATRMATCH,
    SCARD_STATE_EXCLUSIVE,
    SCARD_STATE_INUSE,
    SCARD_STATE_MUTE
} StateType ;

// SCARD_STATE_UNPOWERED is not defined on Windows and old Mac OS X
%constant unsigned long SCARD_STATE_UNPOWERED = 0x0400 ;

// protocols
#ifdef WIN32
typedef enum
{
    SCARD_PROTOCOL_UNDEFINED,
    SCARD_PROTOCOL_T0,
    SCARD_PROTOCOL_T1,
    SCARD_PROTOCOL_RAW,
    SCARD_PROTOCOL_Tx,
    SCARD_PROTOCOL_DEFAULT,
    SCARD_PROTOCOL_OPTIMAL
} ProtocolType ;

// define pcsc lite constants for winscard
%constant unsigned long SCARD_PROTOCOL_UNSET = SCARD_PROTOCOL_UNDEFINED ;
%constant unsigned long SCARD_PROTOCOL_ANY = SCARD_PROTOCOL_Tx ;
%constant unsigned long SCARD_PROTOCOL_T15 = 0x00000008 ;
#endif

#ifdef PCSCLITE
    #ifdef __APPLE__
        typedef enum
        {
            SCARD_PROTOCOL_T0,
            SCARD_PROTOCOL_T1,
            SCARD_PROTOCOL_RAW,
            SCARD_PROTOCOL_ANY
        } ProtocolType ;
        %constant unsigned long SCARD_PROTOCOL_UNSET = SCARD_PROTOCOL_ANY ;
        %constant unsigned long SCARD_PROTOCOL_T15 = 0x00000008 ;
        %constant unsigned long SCARD_PROTOCOL_UNDEFINED = 0 ;
        %constant unsigned long SCARD_PROTOCOL_OPTIMAL = SCARD_PROTOCOL_ANY ;
    #else //__APPLE__
        typedef enum
        {
            SCARD_PROTOCOL_UNSET,
            SCARD_PROTOCOL_T0,
            SCARD_PROTOCOL_T1,
            SCARD_PROTOCOL_RAW,
            SCARD_PROTOCOL_T15,
            SCARD_PROTOCOL_ANY
        } ProtocolType ;
        %constant unsigned long SCARD_PROTOCOL_UNDEFINED = SCARD_PROTOCOL_UNSET ;
        %constant unsigned long SCARD_PROTOCOL_OPTIMAL = SCARD_PROTOCOL_UNSET ;
    #endif //!__APPLE__
    // define winscard constants for pcsc lite
    %constant unsigned long SCARD_PROTOCOL_Tx = SCARD_PROTOCOL_ANY ;
    %constant unsigned long SCARD_PROTOCOL_DEFAULT = SCARD_PROTOCOL_ANY ;
#endif //PCSCLITE


%constant unsigned long SCARD_PCI_T0 = 0x01 ;
%constant unsigned long SCARD_PCI_T1 = 0x02 ;
%constant unsigned long SCARD_PCI_RAW = 0x04 ;


#ifdef WIN32

typedef enum
{
    SCARD_PROVIDER_PRIMARY,
    SCARD_PROVIDER_CSP
} ProviderType ;


typedef enum
{
    SCARD_ATTR_VENDOR_NAME,
    SCARD_ATTR_VENDOR_IFD_TYPE,
    SCARD_ATTR_VENDOR_IFD_VERSION,
    SCARD_ATTR_VENDOR_IFD_SERIAL_NO,
    SCARD_ATTR_CHANNEL_ID,
    SCARD_ATTR_DEFAULT_CLK,
    SCARD_ATTR_MAX_CLK,
    SCARD_ATTR_DEFAULT_DATA_RATE,
    SCARD_ATTR_MAX_DATA_RATE,
    SCARD_ATTR_MAX_IFSD,
    SCARD_ATTR_POWER_MGMT_SUPPORT,
    SCARD_ATTR_USER_TO_CARD_AUTH_DEVICE,
    SCARD_ATTR_USER_AUTH_INPUT_DEVICE,
    SCARD_ATTR_CHARACTERISTICS,
    SCARD_ATTR_CURRENT_PROTOCOL_TYPE,
    SCARD_ATTR_CURRENT_CLK,
    SCARD_ATTR_CURRENT_F,
    SCARD_ATTR_CURRENT_D,
    SCARD_ATTR_CURRENT_N,
    SCARD_ATTR_CURRENT_W,
    SCARD_ATTR_CURRENT_IFSC,
    SCARD_ATTR_CURRENT_IFSD,
    SCARD_ATTR_CURRENT_BWT,
    SCARD_ATTR_CURRENT_CWT,
    SCARD_ATTR_CURRENT_EBC_ENCODING,
    SCARD_ATTR_EXTENDED_BWT,
    SCARD_ATTR_ICC_PRESENCE,
    SCARD_ATTR_ICC_INTERFACE_STATUS,
    SCARD_ATTR_CURRENT_IO_STATE,
    SCARD_ATTR_ATR_STRING,
    SCARD_ATTR_ICC_TYPE_PER_ATR,
    SCARD_ATTR_ESC_RESET,
    SCARD_ATTR_ESC_CANCEL,
    SCARD_ATTR_ESC_AUTHREQUEST,
    SCARD_ATTR_MAXINPUT,
    SCARD_ATTR_DEVICE_UNIT,
    SCARD_ATTR_DEVICE_IN_USE,
    SCARD_ATTR_DEVICE_FRIENDLY_NAME_A,
    SCARD_ATTR_DEVICE_SYSTEM_NAME_A,
    SCARD_ATTR_DEVICE_FRIENDLY_NAME_W,
    SCARD_ATTR_DEVICE_SYSTEM_NAME_W,
    SCARD_ATTR_SUPRESS_T1_IFS_REQUEST
} AttributeType ;

typedef enum
{
    // from winerror.h
    ERROR_ALREADY_EXISTS
} ErrorTypeWin32Only;

#endif // WIN32


#ifdef PCSCLITE
    typedef enum
    {
        SCARD_ATTR_VENDOR_NAME              ,
        SCARD_ATTR_VENDOR_IFD_TYPE          ,
        SCARD_ATTR_VENDOR_IFD_VERSION       ,
        SCARD_ATTR_VENDOR_IFD_SERIAL_NO     ,
        SCARD_ATTR_CHANNEL_ID               ,
        SCARD_ATTR_ASYNC_PROTOCOL_TYPES     ,
        SCARD_ATTR_DEFAULT_CLK              ,
        SCARD_ATTR_MAX_CLK                  ,
        SCARD_ATTR_DEFAULT_DATA_RATE        ,
        SCARD_ATTR_MAX_DATA_RATE            ,
        SCARD_ATTR_MAX_IFSD                 ,
        SCARD_ATTR_SYNC_PROTOCOL_TYPES      ,
        SCARD_ATTR_POWER_MGMT_SUPPORT       ,
        SCARD_ATTR_USER_TO_CARD_AUTH_DEVICE ,
        SCARD_ATTR_USER_AUTH_INPUT_DEVICE   ,
        SCARD_ATTR_CHARACTERISTICS          ,
        SCARD_ATTR_CURRENT_PROTOCOL_TYPE    ,
        SCARD_ATTR_CURRENT_CLK              ,
        SCARD_ATTR_CURRENT_F                ,
        SCARD_ATTR_CURRENT_D                ,
        SCARD_ATTR_CURRENT_N                ,
        SCARD_ATTR_CURRENT_W                ,
        SCARD_ATTR_CURRENT_IFSC             ,
        SCARD_ATTR_CURRENT_IFSD             ,
        SCARD_ATTR_CURRENT_BWT              ,
        SCARD_ATTR_CURRENT_CWT              ,
        SCARD_ATTR_CURRENT_EBC_ENCODING     ,
        SCARD_ATTR_EXTENDED_BWT             ,
        SCARD_ATTR_ICC_PRESENCE             ,
        SCARD_ATTR_ICC_INTERFACE_STATUS     ,
        SCARD_ATTR_CURRENT_IO_STATE         ,
        SCARD_ATTR_ATR_STRING               ,
        SCARD_ATTR_ICC_TYPE_PER_ATR         ,
        SCARD_ATTR_ESC_RESET                ,
        SCARD_ATTR_ESC_CANCEL               ,
        SCARD_ATTR_ESC_AUTHREQUEST          ,
        SCARD_ATTR_MAXINPUT                 ,
        SCARD_ATTR_DEVICE_UNIT              ,
        SCARD_ATTR_DEVICE_IN_USE            ,
        SCARD_ATTR_DEVICE_FRIENDLY_NAME_A   ,
        SCARD_ATTR_DEVICE_SYSTEM_NAME_A     ,
        SCARD_ATTR_DEVICE_FRIENDLY_NAME_W   ,
        SCARD_ATTR_DEVICE_SYSTEM_NAME_W     ,
        SCARD_ATTR_SUPRESS_T1_IFS_REQUEST
    } AttributeType ;

    %constant unsigned long SCARD_ATTR_DEVICE_FRIENDLY_NAME = SCARD_ATTR_DEVICE_FRIENDLY_NAME_A ;
    %constant unsigned long SCARD_ATTR_DEVICE_SYSTEM_NAME = SCARD_ATTR_DEVICE_SYSTEM_NAME_A ;
#endif //PCSCLITE


/* int and unsigned long are different on 64-bits systems */
#ifdef __APPLE__
#define TYPE int
#else
#define TYPE long
#endif

%constant TYPE SCARD_S_SUCCESS             = SCARD_S_SUCCESS ;
%constant TYPE SCARD_F_INTERNAL_ERROR      = SCARD_F_INTERNAL_ERROR ;
%constant TYPE SCARD_E_CANCELLED           = SCARD_E_CANCELLED ;
%constant TYPE SCARD_E_INVALID_HANDLE      = SCARD_E_INVALID_HANDLE ;
%constant TYPE SCARD_E_INVALID_PARAMETER   = SCARD_E_INVALID_PARAMETER ;
%constant TYPE SCARD_E_INVALID_TARGET      = SCARD_E_INVALID_TARGET ;
%constant TYPE SCARD_E_NO_MEMORY           = SCARD_E_NO_MEMORY ;
%constant TYPE SCARD_F_WAITED_TOO_LONG     = SCARD_F_WAITED_TOO_LONG ;
%constant TYPE SCARD_E_INSUFFICIENT_BUFFER = SCARD_E_INSUFFICIENT_BUFFER ;
%constant TYPE SCARD_E_UNKNOWN_READER      = SCARD_E_UNKNOWN_READER ;
%constant TYPE SCARD_E_TIMEOUT             = SCARD_E_TIMEOUT ;
%constant TYPE SCARD_E_SHARING_VIOLATION   = SCARD_E_SHARING_VIOLATION ;
%constant TYPE SCARD_E_NO_SMARTCARD        = SCARD_E_NO_SMARTCARD ;
%constant TYPE SCARD_E_UNKNOWN_CARD        = SCARD_E_UNKNOWN_CARD ;
%constant TYPE SCARD_E_CANT_DISPOSE        = SCARD_E_CANT_DISPOSE ;
%constant TYPE SCARD_E_PROTO_MISMATCH      = SCARD_E_PROTO_MISMATCH ;
%constant TYPE SCARD_E_NOT_READY           = SCARD_E_NOT_READY ;
%constant TYPE SCARD_E_INVALID_VALUE       = SCARD_E_INVALID_VALUE ;
%constant TYPE SCARD_E_SYSTEM_CANCELLED    = SCARD_E_SYSTEM_CANCELLED ;
%constant TYPE SCARD_F_COMM_ERROR          = SCARD_F_COMM_ERROR ;
%constant TYPE SCARD_F_UNKNOWN_ERROR       = SCARD_F_UNKNOWN_ERROR ;
%constant TYPE SCARD_E_INVALID_ATR         = SCARD_E_INVALID_ATR ;
%constant TYPE SCARD_E_NOT_TRANSACTED      = SCARD_E_NOT_TRANSACTED ;
%constant TYPE SCARD_E_READER_UNAVAILABLE  = SCARD_E_READER_UNAVAILABLE ;
%constant TYPE SCARD_E_PCI_TOO_SMALL       = SCARD_E_PCI_TOO_SMALL ;
%constant TYPE SCARD_E_READER_UNSUPPORTED  = SCARD_E_READER_UNSUPPORTED ;
%constant TYPE SCARD_E_DUPLICATE_READER    = SCARD_E_DUPLICATE_READER ;
%constant TYPE SCARD_E_CARD_UNSUPPORTED    = SCARD_E_CARD_UNSUPPORTED ;
%constant TYPE SCARD_E_NO_SERVICE          = SCARD_E_NO_SERVICE ;
%constant TYPE SCARD_E_SERVICE_STOPPED     = SCARD_E_SERVICE_STOPPED ;
#ifdef SCARD_E_NO_READERS_AVAILABLE
%constant TYPE SCARD_E_NO_READERS_AVAILABLE = SCARD_E_NO_READERS_AVAILABLE ;
#else
%constant TYPE SCARD_E_NO_READERS_AVAILABLE = 0x8010002E ;
#endif
%constant TYPE SCARD_E_UNSUPPORTED_FEATURE = SCARD_E_UNSUPPORTED_FEATURE ;
%constant TYPE SCARD_W_UNSUPPORTED_CARD    = SCARD_W_UNSUPPORTED_CARD ;
%constant TYPE SCARD_W_UNRESPONSIVE_CARD   = SCARD_W_UNRESPONSIVE_CARD ;
%constant TYPE SCARD_W_UNPOWERED_CARD      = SCARD_W_UNPOWERED_CARD ;
%constant TYPE SCARD_W_RESET_CARD          = SCARD_W_RESET_CARD ;
%constant TYPE SCARD_W_REMOVED_CARD        = SCARD_W_REMOVED_CARD ;

#ifdef SCARD_W_SECURITY_VIOLATION
/* introduced in pcsc-lite > 1.5.2 */
%constant TYPE SCARD_W_SECURITY_VIOLATION  = SCARD_W_SECURITY_VIOLATION ;
%constant TYPE SCARD_W_WRONG_CHV           = SCARD_W_WRONG_CHV ;
%constant TYPE SCARD_W_CHV_BLOCKED         = SCARD_W_CHV_BLOCKED ;
%constant TYPE SCARD_W_EOF                 = SCARD_W_EOF ;
%constant TYPE SCARD_W_CANCELLED_BY_USER   = SCARD_W_CANCELLED_BY_USER ;
%constant TYPE SCARD_W_CARD_NOT_AUTHENTICATED = SCARD_W_CARD_NOT_AUTHENTICATED ;
%constant TYPE SCARD_E_UNEXPECTED          = SCARD_E_UNEXPECTED ;
%constant TYPE SCARD_E_ICC_INSTALLATION    = SCARD_E_ICC_INSTALLATION ;
%constant TYPE SCARD_E_ICC_CREATEORDER     = SCARD_E_ICC_CREATEORDER ;
%constant TYPE SCARD_E_DIR_NOT_FOUND       = SCARD_E_DIR_NOT_FOUND ;
%constant TYPE SCARD_E_FILE_NOT_FOUND      = SCARD_E_FILE_NOT_FOUND ;
%constant TYPE SCARD_E_NO_DIR              = SCARD_E_NO_DIR ;
%constant TYPE SCARD_E_NO_FILE             = SCARD_E_NO_FILE ;
%constant TYPE SCARD_E_NO_ACCESS           = SCARD_E_NO_ACCESS ;
%constant TYPE SCARD_E_WRITE_TOO_MANY      = SCARD_E_WRITE_TOO_MANY ;
%constant TYPE SCARD_E_BAD_SEEK            = SCARD_E_BAD_SEEK ;
%constant TYPE SCARD_E_INVALID_CHV         = SCARD_E_INVALID_CHV ;
%constant TYPE SCARD_E_UNKNOWN_RES_MNG     = SCARD_E_UNKNOWN_RES_MNG ;
%constant TYPE SCARD_E_NO_SUCH_CERTIFICATE = SCARD_E_NO_SUCH_CERTIFICATE ;
%constant TYPE SCARD_E_CERTIFICATE_UNAVAILABLE = SCARD_E_CERTIFICATE_UNAVAILABLE ;
%constant TYPE SCARD_E_COMM_DATA_LOST      = SCARD_E_COMM_DATA_LOST ;
%constant TYPE SCARD_E_NO_KEY_CONTAINER    = SCARD_E_NO_KEY_CONTAINER ;
%constant TYPE SCARD_E_SERVER_TOO_BUSY     = SCARD_E_SERVER_TOO_BUSY ;
#else
%constant TYPE SCARD_W_SECURITY_VIOLATION  = 0x8010006A ;
%constant TYPE SCARD_W_WRONG_CHV           = 0x8010006B ;
%constant TYPE SCARD_W_CHV_BLOCKED         = 0x8010006C ;
%constant TYPE SCARD_W_EOF                 = 0x8010006D ;
%constant TYPE SCARD_W_CANCELLED_BY_USER   = 0x8010006E ;
%constant TYPE SCARD_W_CARD_NOT_AUTHENTICATED = 0x8010006F ;
%constant TYPE SCARD_E_UNEXPECTED          = 0x8010001F ;
%constant TYPE SCARD_E_ICC_INSTALLATION    = 0x80100020 ;
%constant TYPE SCARD_E_ICC_CREATEORDER     = 0x80100021 ;
%constant TYPE SCARD_E_DIR_NOT_FOUND       = 0x80100023 ;
%constant TYPE SCARD_E_FILE_NOT_FOUND      = 0x80100024 ;
%constant TYPE SCARD_E_NO_DIR              = 0x80100025 ;
%constant TYPE SCARD_E_NO_FILE             = 0x80100026 ;
%constant TYPE SCARD_E_NO_ACCESS           = 0x80100027 ;
%constant TYPE SCARD_E_WRITE_TOO_MANY      = 0x80100028 ;
%constant TYPE SCARD_E_BAD_SEEK            = 0x80100029 ;
%constant TYPE SCARD_E_INVALID_CHV         = 0x8010002A ;
%constant TYPE SCARD_E_UNKNOWN_RES_MNG     = 0x8010002B ;
%constant TYPE SCARD_E_NO_SUCH_CERTIFICATE = 0x8010002C ;
%constant TYPE SCARD_E_CERTIFICATE_UNAVAILABLE = 0x8010002D ;
%constant TYPE SCARD_E_COMM_DATA_LOST      = 0x8010002F ;
%constant TYPE SCARD_E_NO_KEY_CONTAINER    = 0x80100030 ;
%constant TYPE SCARD_E_SERVER_TOO_BUSY     = 0x80100031 ;
#endif

#ifdef WIN32
typedef enum
{
    ERROR_INVALID_HANDLE
} Win32ErrorType ;
#endif //WIN32
#ifdef PCSCLITE
%constant unsigned long INVALID_HANDLE = SCARD_E_INVALID_HANDLE ;
#endif //PCSCLITE

// this error code is defined outside the enum, since it is available
// on winscard only (e.g. not in pcsc lite)
%constant unsigned long SCARD_P_SHUTDOWN = 0x80100018 ;

// Infinite timeout
%constant unsigned long INFINITE = 0x7FFFFFFF ;
