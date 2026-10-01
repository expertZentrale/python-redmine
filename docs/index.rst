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
project management application. Redmine exposes some data via `REST API
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

* Supports 100% of Redmine API, up to Redmine 7.0
* Supports external Redmine plugins API: ``redmine_expert_helpdesk``, ``redmine_expert_agile`` and the RedmineUP
  CRM, Helpdesk, Agile, Checklists and Questions plugins
* Supports Python 3.10 - 3.14 and PyPy3
* Supports different request engines
* Extendable via custom resources and custom request engines
* Extensively documented
* Provides ORM-style Pythonic API
* And many more...

Acknowledgements
----------------

A big thank you to `Maxim Tepkeev <https://github.com/maxtepkeev>`__, who created Python-Redmine and maintained
it from 2014 to 2024. His work made a well-designed, thoroughly tested and extensively documented library
available to everyone. This fork only exists because his foundation was solid enough to build on, and the
vast majority of its code is still his. Thanks as well to everyone who contributed to the
`original project <https://github.com/maxtepkeev/python-redmine>`__.

Copyright and License
---------------------

Licensed under the Apache 2.0 license. Check the :doc:`license` for details.

Table of contents
-----------------

.. toctree::
   :maxdepth: 3

   installation
   configuration
   introduction
   resources/index
   advanced/index
   FAQ <faq>
   exceptions
   license
   changelog
