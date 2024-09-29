pyscard: smartcard library for python
=====================================

https://pyscard.sourceforge.io/

Copyright 2001-2012 Gemalto

Authors:

- Jean-Daniel Aussel, jean-daniel.aussel@gemalto.com
- Ludovic Rousseau, ludovic.rousseau@free.fr

This file is part of pyscard.

pyscard is free software; you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the
Free Software Foundation; either version 2.1 of the License, or (at your
option) any later version.

pyscard is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pyscard; if not, write to the Free Software Foundation, Inc.,
51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

pyscard is a python module adding smart cards support to python.

It consists of the `smartcard.scard` module, an extension module wrapping
Windows smart card base components (also known as PCSC) on Windows, and
PCSC lite on GNU/Linux and macOS, and of the smartcard module, a
python framework with objects wrapping PCSC API.


Documentation
-------------
All documentation is provided in the `src/smartcard/doc` directory of the
source distribution.  Examples are provided in the `src/smartcard/Examples`
directory of the source distribution.  The binary distribution does not
include any documentation, tests scripts or examples.


Installation
------------
The pyscard library is packaged using the standard setuptools python
module.

Installation on windows
-----------------------

Installing on windows from the binary distribution
--------------------------------------------------

Use pip:
```
pip install pyscard
```

Installing on windows from the source distribution
---------------------------------------------------

1. you will need [swig](https://www.swig.org/), and a C compiler.

You can install swig using:

* Install the chocolately package manager
* Open a powershell as administrator mode, run
```
choco install swig
```
* Then in the same window, install pyscard by
```
pip install pyscard
```

2. download the source distribution

The source distribution is available `pyscard-1.9.<xx>.tar.gz` for Windows and GNU/Linux.

3. unzip the source distribution, open a console and type the following:

```
setup.py build_ext install
```

This will build pyscard and install it in the site-packages directory of
your python distribution, e.g. `c:\python312\Lib\site-packages\smartcard`.

This install procedure does not install the documentation, examples or test
files.

Installation on GNU/Linux or macOS
----------------------------------

Installing on GNU/Linux or macOS from the source distribution
-------------------------------------------------------------

1. you will need gcc, swig (https://www.swig.org/), and pcsc-lite
(https://pcsclite.apdu.fr/)

2. download the source distribution

The source distribution is available as `pyscard-1.9.<xx>.tar.gz`.

3. untar the source distribution

4. from a terminal with root privileges, type the following:

```
sudo python setup.py install
```

This will build pyscard and install it in the site-packages directory of
your python distribution, e.g.
`/usr/lib/python3.12/site-packages/smartcard`.

Developer documentation, unit tests and examples
------------------------------------------------
The developer documentation is in the `src/smartcard/doc/` directory of the
source distribution.

Examples are located in the `src/smartcard/Examples/` directory, and the pyunit
unit tests in the `src/smartcard/test/` directory.

Build instructions for packagers
--------------------------------

Building a binary distribution for Windows
------------------------------------------

To build a binary distribution from the source distribution, you will
need a C compiler and swig (same requirements as for installing
from the source distribution).

In the root directory of the source distribution, execute the following
command in a console:

```
python -m build
```

This will build the wheel installer with a name similar to `pyscard-2.0.5-cp311-cp311-win_amd64.whl` in the `dist/`directory.

Building a binary distribution for GNU/Linux
--------------------------------------------

To build a binary distribution from the source distribution, you will
need gcc, swig and pcsc-lite (same requirements as for installing
from the source distribution).

In the root directory of the source distribution, execute the following
command in a terminal:

```
python3 -m venv temp
source temp/bin/activate
pip3 install -r dev-requirements.txt
python3 -m build
```

This will build a wheel installer with a name similar to `pyscard-2.0.7-cp310-cp310-linux_x86_64.whl` and a source code archive `pyscard-2.0.7.tar.gz` in the `dist/`directory.

Building a binary distribution for macOS
----------------------------------------

To build a binary distribution from the source distribution, you will
need swig and Xcode (same requirements as for installing from the source
distribution).

The steps are then the same as for GNU/Linux.
