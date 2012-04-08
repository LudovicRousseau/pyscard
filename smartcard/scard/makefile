# -----------------------------------------------------------------------------
# Copyright 2001-2012 gemalto
# Author: Jean-Daniel Aussel, mailto:jean-daniel.aussel@gemalto.com
#
# A little makefile to build the python extension outside of distutils
# on windows for easy debugging.
#
# This file is part of pyscard.
#
# pyscard is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# pyscard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyscard; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# -----------------------------------------------------------------------------

# where python and swig are located usually on my machine
# adapt to your configuration
# the pythondev must contain the debug libraries (e.g. python25_d.lib)
pythondir=c:\projects\pyscard\factory\python
pythondebugdir=c:\projects\pyscard\factory\pythondev
pythonpackagedir=$(pythondir)\Lib\site-packages\smartcard\scard
swigdir=c:\projects\pyscard\factory\swig

# common compiler and linker flags
linker_flags = /DLL /nologo /INCREMENTAL:no /LIBPATH:$(pythondir)\libs /LIBPATH:$(pythondebugdir)\libs

# final target
all: $(pythonpackagedir)\_scard.pyd $(pythonpackagedir)\_scard_d.pyd

# depedencies
$(pythonpackagedir)\_scard.pyd : obj\_scard.pyd
	if exist obj\_scard.pyd copy obj\_scard.pyd $(pythonpackagedir)\_scard.pyd

$(pythonpackagedir)\_scard_d.pyd  : objd\_scard_d.pyd
	if exist objd\_scard_d.pyd copy objd\_scard_d.pyd $(pythonpackagedir)\_scard_d.pyd
	if exist objd\_scard_d.pdb copy objd\_scard_d.pyd $(pythonpackagedir)\_scard_d.pdb

obj\_scard.pyd : obj\scard_wrap.obj obj\helpers.obj obj\winscarddll.obj obj\scard.res
	link.exe $(linker_flags) /EXPORT:init_scard $** /OUT:$@ /IMPLIB:$*.lib

objd\_scard_d.pyd : objd\scard_wrap.obj objd\helpers.obj objd\winscarddll.obj objd\scard.res
	link.exe $(linker_flags) /DEBUG winscard.lib /EXPORT:init_scard $** /OUT:$@ /IMPLIB:$*.lib

obj\scard_wrap.obj : obj\scard_wrap.c

objd\scard_wrap.obj : objd\scard_wrap.c

objd\helpers.obj obj\helpers.obj : helpers.c

objd\winscarddll.obj obj\winscarddll.obj : winscarddll.c

objd\scard.res obj\scard.res : scard.rc

obj\scard_wrap.c: scard.i pcscdefs.i pcsctypemaps.i
	if not exist obj mkdir obj
	swig.exe -python -outdir obj -DWIN32 -o obj/scard_wrap.c scard.i

objd\scard_wrap.c: scard.i pcscdefs.i pcsctypemaps.i
	if not exist objd mkdir objd
	swig.exe -python -outdir objd -DWIN32 -o objd/scard_wrap.c scard.i

# inference rules
.SUFFIXES: .i

.c{obj}.obj:
	if not exist obj mkdir obj
	cl.exe /c /nologo /Ox /MD /W3 /GX /DNDEBUG -DWIN32=100 -I$(pythondir)\include /Tc$< /Fo$@

.c{objd}.obj:
	if not exist objd mkdir objd
	cl.exe /c /nologo /Od /MDd /W3 /GX /Z7 -DWIN32=100 -I./ -I$(pythondir)\include /Tc$< /Fo$@

{obj}.c{obj}.obj:
	if not exist obj mkdir obj
	cl.exe /c /nologo /Ox /MD /W3 /GX /DNDEBUG -DWIN32=100 -I$(pythondir)\include -I. /Tc$< /Fo$@

{objd}.c{objd}.obj:
	if not exist objd mkdir objd
	cl.exe /c /nologo /Od /MDd /W3 /GX /Z7 -DWIN32=100 -I./ -I$(pythondir)\include -I. /Tc$< /Fo$@

.rc{obj}.res:
	if not exist obj mkdir obj
	rc.exe -DWIN32=100 -Ismartcard/scard/ -I$(pythondir)\include /fo$@ $<

.rc{objd}.res:
	if not exist objd mkdir objd
	rc.exe -DWIN32=100 -Ismartcard/scard/ -I$(pythondir)\include /fo$@ $<

# clean-up generated files
clean:
	@del obj\_scard.pyd obj\_scard.exp obj\_scard.lib
	@del obj\scard_wrap.obj obj\helpers.obj obj\winscarddll.obj
	@del obj\scard.res obj\scard.py obj\scard_wrap.c
	@del objd\_scard_d.pyd objd\_scard_d.exp objd\_scard_d.lib
	@del objd\_scard_d.pdb objd\scard_wrap.obj objd\helpers.obj objd\winscarddll.obj
	@del objd\scard.res objd\scard.py objd\scard_wrap.c
