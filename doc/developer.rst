.. toctree::

.. highlight:: sh

===============
Developer Guide
===============


Setup Development Environment
=============================

#. Install ``pip`` and ``tox``:

   ::

      sudo apt-get install python-pip
      sudo pip install tox

#. Configure git pre-commit hook:

   ::

      sudo pip install flake8 pep8-naming
      flake8 --install-hook
      git config flake8.strict true


Launching executable from repository
====================================

To execute ``tse2sql`` from the repository you can:

#. Install dependencies system-wide:

   ::

      sudo pip install -r requirements.txt
      PYTHONPATH=lib/ bin/tse2sql

#. Load the ``py34`` virtual environment:

   ::

      tox -e py34
      source .tox/py34/bin/activate
      PYTHONPATH=lib/ bin/tse2sql


Building Documentation
======================

::

   tox -e doc

Output will be available at ``.tox/doc/tmp/html``. It is recommended to install
the ``webdev`` package:

::

   sudo pip install webdev

So a development web server can serve any location like this:

::

   $ webdev .tox/doc/tmp/html


Running Test Suite
==================

::

   tox -e py27,py34
