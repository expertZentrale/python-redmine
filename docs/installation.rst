Installation
============

Dependencies
------------

Python-Redmine relies heavily on great `Requests <http://docs.python-requests.org>`_ library by Kenneth Reitz
for all the http(s) calls.

Installation
------------

The expert fork is distributed as ``python-redmine-expert`` and provides the same ``redminelib`` package
as upstream ``python-redmine``, so uninstall the latter first if present. Released versions are published
as `GitHub releases <https://github.com/expertZentrale/python-redmine/releases>`_ with the wheel attached:

.. code-block:: bash

   $ pip uninstall python-redmine
   $ pip install https://github.com/expertZentrale/python-redmine/releases/download/v3.1.1/python_redmine_expert-3.1.1-py3-none-any.whl

Or install straight from a tag, which is also the form to use in ``requirements.txt`` or ``pyproject.toml``:

.. code-block:: bash

   $ pip install "python-redmine-expert @ git+https://github.com/expertZentrale/python-redmine.git@v3.1.1"

From a local checkout:

.. code-block:: bash

   $ git clone https://github.com/expertZentrale/python-redmine.git
   $ cd python-redmine
   $ pip install .
