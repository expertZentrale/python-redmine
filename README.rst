Python-Redmine (expert fork)
============================

|Tests|

.. |Tests| image:: https://img.shields.io/github/actions/workflow/status/expertZentrale/python-redmine/tests.yml.svg
   :target: https://github.com/expertZentrale/python-redmine/actions/workflows/tests.yml

This is the expert fork of `Python-Redmine <https://github.com/maxtepkeev/python-redmine>`__, maintained for
internal use after upstream development stopped. It is distributed as ``python-redmine-expert`` while keeping the
``redminelib`` import name, so it is a drop-in replacement for ``python-redmine``. On top of upstream it adds
support for the ``redmine_expert_helpdesk`` and ``redmine_expert_agile`` plugins.

Python-Redmine is a library for communicating with a `Redmine <http://www.redmine.org>`__
project management application. Redmine exposes some of its data via `REST API
<http://www.redmine.org/projects/redmine/wiki/Rest_api>`__ for which Python-Redmine provides
a simple but powerful Pythonic API inspired by a well-known `Django ORM
<https://docs.djangoproject.com/en/dev/topics/db/queries/>`__:

.. code-block:: python

   >>> from redminelib import Redmine

   >>> redmine = Redmine('http://demo.redmine.org', username='foo', password='bar')
   >>> project = redmine.project.get('vacation')

   >>> project.id
   30404

   >>> project.identifier
   'vacation'

   >>> project.created_on
   datetime.datetime(2013, 12, 31, 13, 27, 47)

   >>> project.issues
   <redminelib.resultsets.ResourceSet object with Issue resources>

   >>> project.issues[0]
   <redminelib.resources.Issue #34441 "Vacation">

   >>> dir(project.issues[0])
   ['assigned_to', 'author', 'created_on', 'description', 'done_ratio',
   'due_date', 'estimated_hours', 'id', 'priority', 'project', 'relations',
   'start_date', 'status', 'subject', 'time_entries', 'tracker', 'updated_on']

   >>> project.issues[0].subject
   'Vacation'

   >>> project.issues[0].time_entries
   <redminelib.resultsets.ResourceSet object with TimeEntry resources>

Features
--------

* Supports 100% of Redmine API
* Supports external Redmine plugins API, including ``redmine_expert_helpdesk`` and ``redmine_expert_agile``
* Supports Python 3.10 - 3.14 and PyPy3
* Supports different request engines
* Extendable via custom resources and custom request engines
* Extensively documented
* Provides ORM-style Pythonic API
* And many more...

Installation
------------

Uninstall ``python-redmine`` first if present, both distributions provide the ``redminelib`` package:

.. code-block:: bash

   $ pip uninstall python-redmine
   $ pip install git+https://github.com/expertZentrale/python-redmine.git@master

Development
-----------

.. code-block:: bash

   $ python -m venv .venv && . .venv/bin/activate
   $ pip install -e '.[dev]'
   $ pytest
   $ ruff check . && ruff format --check .
   $ sphinx-build -b html -n -W docs docs/_build

Documentation
-------------

Documentation sources live in the ``docs`` directory and can be built with Sphinx as shown above.

Copyright and License
---------------------

Licensed under the Apache 2.0 license, see ``LICENSE``. Originally written by Maxim Tepkeev, modifications
by expert Zentrale.
