Helpdesk Knowledge Base Entry
=============================

.. versionadded:: 3.3.0

Requires Redmine >= 5.0 and the ``redmine_expert_helpdesk`` plugin >= 0.23.0. Reading requires the
``view_helpdesk_kb`` permission, creating, updating, approving and rejecting ``edit_helpdesk_kb``,
deleting, reindexing and re-extracting ``manage_helpdesk_kb``.

The plugin keeps the entry in its database and a copy of the approved ones in a vector store. Every
write re-embeds an approved entry and removes any other one from the vector store, the entry returned
by a write carries the outcome in ``vector_sync``:

* ``indexed`` - approved and embedded, searchable with the new text
* ``removed`` - not approved and not in the vector store
* ``not_configured`` - approved, but the knowledge base is switched off or not configured
* ``problem_blank`` - approved, but there is no problem text to embed
* ``index_failed`` - approved, but embedding failed, retry or reindex
* ``unindex_failed`` - not approved, but removing it from the vector store failed

Manager
-------

All operations on the HelpdeskKbEntry resource are provided by its manager. To get access to it
you have to call ``redmine.helpdesk_kb_entry`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new HelpdeskKbEntry resource with given fields. Entries created through the API count as
   curated, so closing the ticket again does not overwrite them with a new extraction.

   :param project_id: (required). Id or identifier of entry's project.
   :type project_id: int or string
   :param int issue_id: (required). Id of a ticket of the project, one entry per ticket.
   :param string problem: (optional). Problem description, this is the text that is embedded.
   :param string solution: (optional). Solution.
   :param string status: (optional). One of ``approved`` or ``pending`` (default).
   :return: :ref:`Resource` object

.. code-block:: python

   >>> entry = redmine.helpdesk_kb_entry.create(
   ...     project_id='support',
   ...     issue_id=4711,
   ...     problem='VPN connection drops after 10 minutes',
   ...     solution='Lowered the MTU on the client to 1400',
   ...     status='approved'
   ... )
   >>> entry
   <redminelib.resources.HelpdeskKbEntry #17 "approved">
   >>> entry.vector_sync
   'indexed'

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single HelpdeskKbEntry resource by its id.

   :param int resource_id: (required). Id of the entry.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> entry = redmine.helpdesk_kb_entry.get(17)
   >>> entry.issue
   <redminelib.resources.Issue #4711 "Printer offline">
   >>> entry.indexed
   True

.. hint::

   The ``issue`` contains the ticket's ``subject`` only if the user may see the ticket.

all
+++

Not supported by the Helpdesk plugin

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns HelpdeskKbEntry resources of a project, most recently changed first.

   :param project_id: (required). Id or identifier of entries' project.
   :type project_id: int or string
   :param string status: (optional). One of ``pending``, ``approved``, ``skipped``, ``rejected``
    (comma-separated for several) or ``all``. Entries with status ``skipped`` are hidden by default.
   :param string q: (optional). Case-insensitive text search in problem and solution.
   :param string issue_id: (optional). Only entries of these tickets, comma-separated.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> entries = redmine.helpdesk_kb_entry.filter(project_id='support', status='pending', q='printer')

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a HelpdeskKbEntry resource. Unlike most resources the plugin
   answers with the updated entry, which is returned.

   :param int resource_id: (required). Entry id.
   :param string problem: (optional). Problem description.
   :param string solution: (optional). Solution.
   :param string status: (optional). One of ``approved`` or ``pending``, use ``reject()`` to reject.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> entry = redmine.helpdesk_kb_entry.update(17, solution='Installed driver 4.2')
   >>> entry.vector_sync
   'indexed'

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.HelpdeskKbEntry
   :noindex:

   Saves current state of a HelpdeskKbEntry resource, an update takes over the entry the plugin
   returns, including ``vector_sync``.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> entry = redmine.helpdesk_kb_entry.get(17)
   >>> entry.save(problem='Network printer prints nothing')
   <redminelib.resources.HelpdeskKbEntry #17 "approved">
   >>> entry.vector_sync
   'indexed'

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single HelpdeskKbEntry resource by its id. If the entry can't be removed from the vector
   store it is kept and a ``ValidationError`` is raised.

   :param int resource_id: (required). Entry id.
   :return: True

Other methods
-------------

approve / reject
++++++++++++++++

.. py:method:: approve(entry_id)
   :module: redminelib.managers.HelpdeskKbEntryManager
   :noindex:

   Approves an entry, which embeds it into the vector store.

   :param int entry_id: (required). Entry id.
   :return: :ref:`Resource` object

.. py:method:: reject(entry_id)
   :module: redminelib.managers.HelpdeskKbEntryManager
   :noindex:

   Rejects an entry, which removes it from the vector store. A rejected entry is kept, so closing
   its ticket again does not bring it back.

   :param int entry_id: (required). Entry id.
   :return: :ref:`Resource` object

Both are also available on the resource, which then takes over the returned entry:

.. code-block:: python

   >>> redmine.helpdesk_kb_entry.approve(17).vector_sync
   'indexed'
   >>> entry = redmine.helpdesk_kb_entry.get(17)
   >>> entry.reject().status
   'rejected'

reindex
+++++++

.. py:method:: reindex(project_id)
   :module: redminelib.managers.HelpdeskKbEntryManager
   :noindex:

   Queues the rebuild of a project's vector index, which re-embeds every approved entry in the
   background. Raises ``ValidationError`` if the knowledge base is not configured.

   :param project_id: (required). Id or identifier of the project.
   :type project_id: int or string
   :return: dict with ``action``, ``queued`` and ``count`` (number of approved entries)

.. code-block:: python

   >>> redmine.helpdesk_kb_entry.reindex('support')
   {'action': 'reindex', 'queued': True, 'count': 42}

reextract
+++++++++

.. py:method:: reextract(project_id, all=False)
   :module: redminelib.managers.HelpdeskKbEntryManager
   :noindex:

   Queues the AI re-extraction of the entries that are not at the project's current detail level,
   with ``all=True`` of every eligible entry. Curated and rejected entries are never re-extracted.
   Each entry costs one AI call. Raises ``ValidationError`` if the knowledge base is not configured.

   :param project_id: (required). Id or identifier of the project.
   :type project_id: int or string
   :param bool all: (optional). Re-extract every eligible entry.
   :return: dict with ``action``, ``queued`` and ``count``, ``queued`` is False if there was nothing
    to re-extract

.. code-block:: python

   >>> redmine.helpdesk_kb_entry.reextract('support', all=True)
   {'action': 'reextract', 'queued': True, 'count': 7}

Export
------

Not supported by the Helpdesk plugin
