.. _framework_samples:

pyscard smartcard framework samples
===================================

pyscard is a python module adding smart cards support to python.

It consists of smartcard.scard, an extension module wrapping Windows
smart card base components (also known as PCSC), and smartcard, a python
framework library hiding PCSC complexity.

Display the ATR of inserted cards
"""""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/simple/getATR.py


Selecting the DF_TELECOM of a card
""""""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/simple/selectDF_TELECOM.py


A simple apdu tracer and interpreter
""""""""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/framework/sample_apduTracerInterpreter.py


Tracing connection events
"""""""""""""""""""""""""

.. literalinclude:: ../Examples/framework/sample_ConsoleConnectionTracer.py


Decorating Card Connections to add custom behavior
""""""""""""""""""""""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/framework/sample_CardConnectionDecorator.py


Detecting response apdu errors
""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/framework/sample_ErrorChecking.py


Implementing a custom ErrorChecker
""""""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/framework/sample_CustomErrorChecker.py


Implementing a custom card type
"""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/framework/sample_CustomCardType.py


Monitoring smartcard readers
""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/framework/sample_MonitorReaders.py


Monitoring smartcard insertion/removal
""""""""""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/framework/sample_MonitorCards.py


APDU/ATR byte to string utilities
"""""""""""""""""""""""""""""""""

.. literalinclude:: ../Examples/framework/sample_toHexString.py

