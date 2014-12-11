.. _wrapper_samples:

PCSC wrapper samples
====================

Using the smartcard framework is the preferred way to write python smart
card application. You can however use the smartcard.scard library to
write your python smart card application if you want to write your own
python framework, or if you want to access some features of the SCardXXX
C API not available in the smartcard framework.

The smartcard.scard module is a native extension module wrapping Windows
smart card base components (also known as PCSC) on Windows, and
pcsc-lite on linux and Mac OS X, whereas the smartcard framework is a
pure python framework hiding scard complexity and PCSC.

send a Control Code to a card or reader
"""""""""""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/scard-api/sample_control.py


get the ATR of a card
"""""""""""""""""""""

.. literalinclude:: ../Examples/scard-api/sample_getATR.py


get the attributes of a card
""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/scard-api/sample_getAttrib.py


wait for card insertion/removal
"""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/scard-api/sample_getStatusChange.py


list the cards introduced in the system
"""""""""""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/scard-api/sample_listCards.py


list the interfaces supported by a card
"""""""""""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/scard-api/sample_listInterfaces.py


locate cards in the system
""""""""""""""""""""""""""

.. literalinclude:: ../Examples/scard-api/sample_locateCards.py


manage readers and reader groups
""""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/scard-api/sample_readerGroups.py


list smart card readers
"""""""""""""""""""""""

.. literalinclude:: ../Examples/scard-api/sample_readers.py


select the DF_TELECOM of a SIM card
"""""""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/scard-api/sample_selectDFTelecom.py


perform a simple smart card transaction
"""""""""""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/scard-api/sample_transaction.py
