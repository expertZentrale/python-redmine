Helpdesk Mailbox
================

.. versionadded:: 3.0.0

Requires Redmine >= 5.0 and the ``redmine_expert_helpdesk`` plugin >= 0.20.0. All operations, including
read ones, require the ``manage_helpdesk`` permission.

Manager
-------

All operations on the HelpdeskMailbox resource are provided by its manager. To get access to it
you have to call ``redmine.helpdesk_mailbox`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new HelpdeskMailbox resource with given fields. See the plugin's ``API.md`` for the complete
   list of fields, the most important ones are listed below. Secrets (``mail_password``,
   ``oauth_client_secret``, ``oauth_sa_key``) are write-only: a blank value keeps the stored secret
   and ``'-'`` clears it, responses only contain ``*_set`` booleans.

   :param project_id: (required). Id or identifier of mailbox's project.
   :type project_id: int or string
   :param string mailbox_address: (required). Mailbox address, globally unique.
   :param string provider: (optional). One of ``graph`` or ``imap``.
   :param bool enabled: (optional). Whether the mailbox is fetched.
   :param string auth_method: (optional). One of ``oauth2`` or ``password``.
   :param string imap_host: (optional). IMAP host.
   :param string mail_password: (optional). Mailbox password (write-only).
   :return: :ref:`Resource` object

.. code-block:: python

   >>> mailbox = redmine.helpdesk_mailbox.create(
   ...     project_id='support',
   ...     mailbox_address='support@example.com',
   ...     provider='imap',
   ...     imap_host='imap.example.com',
   ...     auth_method='password',
   ...     mail_password='secret'
   ... )
   >>> mailbox
   <redminelib.resources.HelpdeskMailbox #7 "support@example.com">

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single HelpdeskMailbox resource by its id.

   :param int resource_id: (required). Id of the mailbox.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> mailbox = redmine.helpdesk_mailbox.get(7)
   >>> mailbox.mail_password_set
   True

all
+++

Not supported by the Helpdesk plugin

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns HelpdeskMailbox resources of a project.

   :param project_id: (required). Id or identifier of mailboxes' project.
   :type project_id: int or string
   :param bool enabled: (optional). Only enabled or disabled mailboxes.
   :param string provider: (optional). Only mailboxes of the provider, ``graph`` or ``imap``.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> mailboxes = redmine.helpdesk_mailbox.filter(project_id='support', enabled=True)

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a HelpdeskMailbox resource. Accepts the same fields as ``create()``
   except ``project_id``.

   :param int resource_id: (required). Mailbox id.
   :return: True

.. code-block:: python

   >>> redmine.helpdesk_mailbox.update(7, enabled=False)
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.HelpdeskMailbox
   :noindex:

   Saves current state of a HelpdeskMailbox resource.

   :return: :ref:`Resource` object

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single HelpdeskMailbox resource by its id.

   :param int resource_id: (required). Mailbox id.
   :return: True

Other methods
-------------

test_connection
+++++++++++++++

.. py:method:: test_connection(mailbox_id)
   :module: redminelib.managers.HelpdeskMailboxManager
   :noindex:

   Tests the connection of a mailbox. A failed test is not raised as an exception but returned with
   ``ok`` set to False.

   :param int mailbox_id: (required). Mailbox id.
   :return: dict with ``ok``, ``message`` and optionally ``folders`` and ``sent_folder``

.. code-block:: python

   >>> redmine.helpdesk_mailbox.test_connection(7)
   {'ok': True, 'message': 'OK', 'folders': ['INBOX', 'Sent']}
   >>> redmine.helpdesk_mailbox.get(7).test_connection()
   {'ok': False, 'message': 'Authentication failed'}

Export
------

Not supported by the Helpdesk plugin
