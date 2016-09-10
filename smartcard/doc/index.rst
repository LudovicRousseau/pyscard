pyscard - Python for smart cards
################################

`pyscard - Python smart card library -
<https://sourceforge.net/projects/pyscard/>`_ is a Python module adding
smart cards support to `Python <http://www.python.org/>`_.

Download
********

The pyscard project is available from different sources:

* pypi `https://pypi.python.org/pypi/pyscard <https://pypi.python.org/pypi/pyscard>`_
* github `https://github.com/LudovicRousseau/pyscard <https://github.com/LudovicRousseau/pyscard>`_
* sourceforge `https://sourceforge.net/projects/pyscard/files/pyscard/ <https://sourceforge.net/projects/pyscard/files/pyscard/>`_

Patch/bug reports
*****************

Report bugs or issues on `github issues
<https://github.com/LudovicRousseau/pyscard/issues>`_ or `sourceforge
<https://sourceforge.net/p/pyscard/bugs/>`_.

Report patches as `github pull requests
<https://github.com/LudovicRousseau/pyscard/pulls>`_ or on `sourceforge
feature requests system
<https://sourceforge.net/p/pyscard/feature-requests/>`_.

Architecture
************

Pyscard consists of:

* `smartcard.scard
  <http://pyscard.sourceforge.net/epydoc/smartcard.scard.scard-module.html>`_,
  an extension module wrapping the WinSCard API (smart card base
  components) also known as PC/SC, and

* `smartcard <http://pyscard.sourceforge.net/epydoc/index.html>`_, a
  higher level Python framework built on top of the raw PC/SC API.

.. image:: ../doc/images/pyscard.jpg
    :align: center

Documentation
*************

    :ref:`pyscard_user_guide`

    `smartcard reference (Python smart card library)
    <http://pyscard.sourceforge.net/epydoc/index.html>`_

    `scard reference (Python PCSC wrapper)
    <http://pyscard.sourceforge.net/epydoc/smartcard.scard.scard-module.html>`_,
    the Python wrapper around PCSC

Samples
*******

    High level API samples: See :ref:`framework_samples`

    Low level API samples: See :ref:`wrapper_samples`

Index
*****

Contents:

.. toctree::
   :maxdepth: 4

   user-guide
   pyscard-framework
   pyscard-wrapper
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

