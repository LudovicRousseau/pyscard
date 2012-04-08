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

#ifndef __MEMLOG_H__
#define __MEMLOG_H__

    #ifdef __cplusplus
    extern "C"
    {
    #endif // __cplusplus

    //
    // define __ENABLE_MEMLOG__ and write your own version
    // of mem_XXX functions to enable memory logging; this
    // is useful to track memory leaks when fiddling with
    // the swig typemaps.
    #ifdef __ENABLE_MEMLOG__
        int mem_CleanUp( void );
        void __cdecl mem_Free( void* pv );
        void mem_HeapCheck( void );
        int mem_Init( void );
        void* __cdecl mem_Malloc( size_t ulSize );
        void* __cdecl mem_MallocWithCaller( size_t ulSize, void* pvCaller );
        void mem_HeapPrint( void );


    //
    // defaults to free/malloc
    //
    #else // !__ENABLE_MEMLOG__
        #define mem_CleanUp() (1)
        #define mem_Free free
        #define mem_HeapCheck()
        #define mem_Init() (1)
        #define mem_Malloc malloc
        #define mem_MallocWithCaller( x, y ) malloc( x )
        #define mem_HeapPrint()

    #endif // __ENABLE_MEMLOG__

    #ifdef __cplusplus
    }
    #endif // __cplusplus

#endif // __MEMLOG_H__
