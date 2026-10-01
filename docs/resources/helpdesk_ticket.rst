Helpdesk Ticket
===============

.. versionadded:: 3.0.0

Requires Redmine >= 5.0 and the ``redmine_expert_helpdesk`` plugin >= 0.20.0. The Helpdesk module has
to be enabled in the project.

A helpdesk ticket is a Redmine issue with helpdesk data attached (contact, mailbox, SLA state and
message history), the ticket id is the issue id.

.. note::

   This resource targets ``redmine_expert_helpdesk`` and is not compatible with RedmineUP's Helpdesk
   plugin, which uses different endpoints and payloads.

Manager
-------

All operations on the HelpdeskTicket resource are provided by its manager. To get access to it
you have to call ``redmine.helpdesk_ticket`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new HelpdeskTicket resource, i.e. a new issue linked to a helpdesk contact. Accepts all
   issue fields (see :doc:`issue`) plus the helpdesk specific fields below. Attachments are not supported.

   :param project_id: (required). Id or identifier of ticket's project.
   :type project_id: int or string
   :param string subject: (required). Ticket subject.
   :param int contact_id: (optional). Id of an existing contact of the same project.
   :param string contact_email: (optional). Email of the contact, the contact is created if it doesn't exist.
   :param string contact_name: (optional). Name used when a new contact is created.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> ticket = redmine.helpdesk_ticket.create(
   ...     project_id='support',
   ...     tracker_id=3,
   ...     subject='Printer on fire',
   ...     description='Please help',
   ...     contact_email='jane@example.com',
   ...     contact_name='Jane Doe'
   ... )
   >>> ticket
   <redminelib.resources.HelpdeskTicket #42 "Printer on fire">

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty HelpdeskTicket resource but saves it only when ``save()`` is called. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single HelpdeskTicket resource by its (issue) id.

   :param int resource_id: (required). Id of the ticket.
   :param list include:
    .. raw:: html

       (optional). Fetches associated data in one call. Accepted values:

    - messages

   :return: :ref:`Resource` object

.. code-block:: python

   >>> ticket = redmine.helpdesk_ticket.get(42, include=['messages'])
   >>> ticket.contact
   <redminelib.resources.HelpdeskContact #1 "Jane Doe">
   >>> ticket.sla['reaction']['status']
   'running'
   >>> ticket.messages[0]['direction']
   'in'

.. hint::

   Messages are lazy loaded if not requested via ``include``, and the full issue is available via the
   ``issue`` attribute:

   .. code-block:: python

      >>> ticket = redmine.helpdesk_ticket.get(42)
      >>> ticket.messages
      [{'id': 9, 'direction': 'in', ...}]
      >>> ticket.issue
      <redminelib.resources.Issue #42 "Printer on fire">

all
+++

Not supported by the Helpdesk plugin

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns visible HelpdeskTicket resources of a project, newest first.

   :param project_id: (required). Id or identifier of tickets' project.
   :type project_id: int or string
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> tickets = redmine.helpdesk_ticket.filter(project_id='support')
   >>> tickets
   <redminelib.resultsets.ResourceSet object with HelpdeskTicket resources>

.. hint::

   For richer filtering use the issue resource, the plugin adds ``helpdesk_kunde``, ``helpdesk_sla_reaction``,
   ``helpdesk_sla_solution`` and ``helpdesk_awaiting_agent`` issue filters, see :doc:`issue`.

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a HelpdeskTicket resource. Accepts the same fields as ``create()``
   (except ``project_id``) and ``notes`` to add a journal note.

   :param int resource_id: (required). Ticket id.
   :return: True

.. code-block:: python

   >>> redmine.helpdesk_ticket.update(42, status_id=2, notes='Replaced toner')
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.HelpdeskTicket
   :noindex:

   Saves current state of a HelpdeskTicket resource.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> ticket = redmine.helpdesk_ticket.get(42)
   >>> ticket.save(assigned_to_id=5)
   <redminelib.resources.HelpdeskTicket #42 "Printer on fire">

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes a HelpdeskTicket and its issue, message history is kept but unlinked.

   :param int resource_id: (required). Ticket id.
   :return: True

.. code-block:: python

   >>> redmine.helpdesk_ticket.delete(42)
   True

Export
------

Not supported by the Helpdesk plugin
