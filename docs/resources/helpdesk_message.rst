Helpdesk Message
================

.. versionadded:: 3.4.0

Requires Redmine >= 5.0 and the ``redmine_expert_helpdesk`` plugin >= 0.26.0. A message is returned when its
ticket is visible to the user (``view_issues``) and the ticket's project has the helpdesk module enabled.

An entry of a ticket's mail log: a customer mail (``direction`` ``in``), a reply sent from Redmine (``out``) or
the assignment of a customer (``init``). The plugin offers no list of the whole mail log, only a lookup by
Message-ID, which tells which ticket a mail went into. A Message-ID that is not found never reached a ticket,
which is what matching a mail server's message trace against Redmine needs.

Manager
-------

All operations on the HelpdeskMessage resource are provided by its manager. To get access to it
you have to call ``redmine.helpdesk_message`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by the Helpdesk plugin

Read methods
------------

get
+++

Not supported by the Helpdesk plugin, ``get(id, message_id=...)`` picks the message out of a ``filter()`` result.

all
+++

Not supported by the Helpdesk plugin

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns the HelpdeskMessage resources with the given Message-IDs, oldest first, across every project the
   user can see. One Message-ID can match several messages, e.g. the same mail received by two projects.

   :param message_id: (required). A Message-ID or a list of them, with or without angle brackets, at most 50
    per call. A list is sent comma-separated.
   :type message_id: string or list
   :param project_id: (optional). Id or identifier of a project to narrow the lookup to.
   :type project_id: int or string
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> messages = redmine.helpdesk_message.filter(message_id=['abc123@mail.example.com', 'unknown@example.com'])
   >>> messages
   <redminelib.resultsets.ResourceSet object with HelpdeskMessage resources>
   >>> message = messages[0]
   >>> message
   <redminelib.resources.HelpdeskMessage #9 "abc123@mail.example.com">
   >>> message.direction, message.issue, message.project
   ('in', <redminelib.resources.Issue #42 "Printer on fire">, <redminelib.resources.Project #1 "Support">)

.. hint::

   ``message_id`` is always returned without angle brackets. To find the Message-IDs that are not in Redmine,
   compare the requested ones without brackets against it.

Update methods
--------------

Not supported by the Helpdesk plugin

Delete methods
--------------

Not supported by the Helpdesk plugin

Export
------

Not supported by the Helpdesk plugin
