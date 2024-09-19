pyscard - Python for smart cards
################################

`pyscard - Python smart card library -
<https://github.com/LudovicRousseau/pyscard>`_ is a Python module adding
smart cards support to `Python <http://www.python.org/>`_ 3.9 and higher.

Download
********

The pyscard project is available from different sources:

* pypi `https://pypi.python.org/pypi/pyscard <https://pypi.python.org/pypi/pyscard>`_
* github `https://github.com/LudovicRousseau/pyscard <https://github.com/LudovicRousseau/pyscard>`_

Patch/bug reports
*****************

Report bugs or issues on `github issues
<https://github.com/LudovicRousseau/pyscard/issues>`_.

Report patches as `github pull requests
<https://github.com/LudovicRousseau/pyscard/pulls>`_.

Architecture
************

Pyscard consists of:

* `smartcard.scard
  <apidocs/smartcard.scard.scard.html>`_,
  an extension module wrapping the WinSCard API (smart card base
  components) also known as PC/SC, and

* `smartcard <apidocs/index.html>`_, a
  higher level Python framework built on top of the raw PC/SC API.

.. image:: ../doc/images/pyscard.jpg
    :align: center

Documentation
*************

    :ref:`pyscard_user_guide`

    `High level API documentation <apidocs/index.html>`_, smartcard
    module

    `Low level API documentation <apidocs/smartcard.scard.scard.html>`_,
    smartcard.scard module

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

