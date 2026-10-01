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

* Supports 100% of Redmine API, up to Redmine 7.0
* Supports external Redmine plugins API: ``redmine_expert_helpdesk``, ``redmine_expert_agile`` and the RedmineUP
  CRM, Helpdesk, Agile, Checklists and Questions plugins
* Supports Python 3.10 - 3.14 and PyPy3
* Supports different request engines
* Extendable via custom resources and custom request engines
* Extensively documented
* Provides ORM-style Pythonic API
* And many more...

Installation
------------

Uninstall ``python-redmine`` first if present, both distributions provide the ``redminelib`` package.
Then install a released version, either the wheel attached to the
`GitHub release <https://github.com/expertZentrale/python-redmine/releases>`__ or straight from the tag:

.. code-block:: bash

   $ pip uninstall python-redmine
   $ pip install https://github.com/expertZentrale/python-redmine/releases/download/v3.2.0/python_redmine_expert-3.2.0-py3-none-any.whl
   # or
   $ pip install "python-redmine-expert @ git+https://github.com/expertZentrale/python-redmine.git@v3.2.0"

In a ``requirements.txt`` or ``pyproject.toml`` pin the tag the same way:

.. code-block:: text

   python-redmine-expert @ git+https://github.com/expertZentrale/python-redmine.git@v3.2.0

Usage
-----

Connect with an API key (*My account* → *API access key*, the REST web service has to be enabled under
*Administration* → *Settings* → *API*):

.. code-block:: python

   from redminelib import Redmine

   redmine = Redmine('https://redmine.example.com', key='<api key>')
   issue = redmine.issue.get(42, include=['journals'])
   issue.save(notes='Looked into it', status_id=2)

``redmine_expert_helpdesk`` (>= 0.20.1):

.. code-block:: python

   ticket = redmine.helpdesk_ticket.create(
       project_id='support', tracker_id=3, subject='Printer on fire',
       description='Please help', contact_email='jane@example.com', contact_name='Jane Doe',
   )
   ticket.contact, ticket.sla, ticket.messages          # contact, SLA state, mail history
   ticket.save(notes='Replaced toner', status_id=2)

   redmine.helpdesk_contact.filter(project_id='support', search='acme')
   redmine.helpdesk_mailbox.get(7).test_connection()     # {'ok': True, 'message': ..., 'folders': [...]}
   redmine.helpdesk_project_setting.update('support', sla_enabled=True, sla_reaction_minutes=120)

   # turn a new issue into a ticket and send the initial mail
   redmine.issue.create(project_id='support', subject='Callback', helpdesk_init={
       'contact_email': 'jane@example.com', 'mailbox_id': 7, 'send_mail': True,
   })

``redmine_expert_agile`` (>= 0.6.1):

.. code-block:: python

   import datetime

   sprint = redmine.expert_agile_sprint.create(
       project_id='scrum', name='Sprint 7',
       start_date=datetime.date(2026, 10, 5), end_date=datetime.date(2026, 10, 16),
   )
   sprint.activate()                                    # status/sharing are plain names: 'active', 'tree', ...
   redmine.expert_agile_sprint.filter(project_id='scrum')

   redmine.expert_agile_data.update(42, story_points=5, sprint_id=sprint.id)
   redmine.issue.create(project_id='scrum', subject='New story',
                        expert_agile_data_attributes={'story_points': 3})
   redmine.issue.filter(project_id='scrum', story_points='>=3')

RedmineUP plugins (CRM, Helpdesk, Agile, Checklists, Questions), with the same API as the former Pro Edition:

.. code-block:: python

   contact = redmine.contact.create(project_id='sales', first_name='Ivan', last_name='Ivanov',
                                    emails=['ivan@example.com'], tag_list=['vip'])
   redmine.deal.create(project_id='sales', name='Big deal', price=1000, contact_id=contact.id, status_id=1)
   redmine.note.create(project_id='sales', source_type='Contact', source_id=contact.id, content='Called him')

   ticket = redmine.ticket.create(issue={'project_id': 'support', 'subject': 'Printer on fire'},
                                  contact={'email': 'ivan@example.com'}, source='phone')
   ticket.reply(content='We are on it')

   redmine.checklist.create(issue_id=42, subject='Passport')
   redmine.agile_sprint.filter(project_id='scrum')

See the `documentation <https://expertzentrale.github.io/python-redmine/>`__ for every resource, method and parameter.

Documentation
-------------

The full documentation is published at https://expertzentrale.github.io/python-redmine/ for every change on
``master``. Its sources are in the ``docs`` directory; build them locally with
``pip install -e '.[docs]' && sphinx-build -b html docs docs/_build``.

Development
-----------

.. code-block:: bash

   $ python -m venv .venv && . .venv/bin/activate
   $ pip install -e '.[dev]'
   $ pytest
   $ ruff check . && ruff format --check .
   $ sphinx-build -b html -n -W docs docs/_build

Releasing
---------

1. Set ``__version__`` in ``redminelib/version.py`` and add the matching ``X.Y.Z (YYYY-MM-DD)`` section to
   ``CHANGELOG.rst``, merge to ``master``.
2. ``git tag -a vX.Y.Z -m 'Release X.Y.Z' && git push origin vX.Y.Z``

The release workflow checks that the tag matches the package version, runs the tests, builds the sdist and
wheel and publishes a GitHub release with the changelog notes and both files attached.

Acknowledgements
----------------

A big thank you to `Maxim Tepkeev <https://github.com/maxtepkeev>`__, who created Python-Redmine and maintained
it from 2014 to 2024. His work made a well-designed, thoroughly tested and extensively documented library
available to everyone. This fork only exists because his foundation was solid enough to build on, and the
vast majority of its code is still his. Thanks as well to everyone who contributed to the
`original project <https://github.com/maxtepkeev/python-redmine>`__.

Copyright and License
---------------------

Licensed under the Apache 2.0 license, see ``LICENSE``. Originally written by Maxim Tepkeev, modifications
by expert Zentrale.
