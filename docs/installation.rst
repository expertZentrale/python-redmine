Installation
============

Dependencies
------------

Python-Redmine relies heavily on great `Requests <http://docs.python-requests.org>`_ library by Kenneth Reitz
for all the http(s) calls.

Installation
------------

The expert fork is distributed as ``python-redmine-expert`` and provides the same ``redminelib`` package
as upstream ``python-redmine``, so uninstall the latter first if present:

.. code-block:: bash

   $ pip uninstall python-redmine
   $ pip install git+https://github.com/expertZentrale/python-redmine.git@master

From a local checkout:

.. code-block:: bash

   $ git clone https://github.com/expertZentrale/python-redmine.git
   $ cd python-redmine
   $ pip install .
