-------------------------------------------------------------------------------
This directory contains the test suite for the pyscard framework.

You will need two smart card readers and two smart cards to run the test
suite.  Insert the readers and the cards in the readers before executing
the test suite.

On the first execution of the test suite, the configcheck.py script in the
parent directory will generate a localconfig.py file that will contain the
current names of the readers and ATRs of the cards inserted in the
readers.  These data are used by the test suite.  If you change the test
configuration, i.e.  add or remove readers or cards, or change the readers
or cards, just delete localconfig.py and re-run the test suite.

-------------------------------------------------------------------------------
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
-------------------------------------------------------------------------------
