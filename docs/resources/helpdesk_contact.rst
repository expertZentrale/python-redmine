Helpdesk Contact
================

.. versionadded:: 3.0.0

Requires Redmine >= 5.0 and the ``redmine_expert_helpdesk`` plugin >= 0.20.0.

Manager
-------

All operations on the HelpdeskContact resource are provided by its manager. To get access to it
you have to call ``redmine.helpdesk_contact`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new HelpdeskContact resource with given fields and saves it to the Helpdesk plugin.
   Requires the ``manage_helpdesk_contacts`` permission.

   :param project_id: (required). Id or identifier of contact's project.
   :type project_id: int or string
   :param string email: (required). Contact email, unique per project, stored lower-cased.
   :param string name: (optional). Contact name.
   :param string company: (optional). Company name.
   :param string phone: (optional). Phone number.
   :param string notes: (optional). Internal notes.
   :param bool info_request_opt_out: (optional). Never send completeness check requests to this contact.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> contact = redmine.helpdesk_contact.create(
   ...     project_id='support',
   ...     email='jane@example.com',
   ...     name='Jane Doe',
   ...     company='ACME'
   ... )
   >>> contact
   <redminelib.resources.HelpdeskContact #1 "Jane Doe">

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty HelpdeskContact resource but saves it to the Helpdesk plugin only when ``save()``
   is called. Valid attributes are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single HelpdeskContact resource from the Helpdesk plugin by its id.

   :param int resource_id: (required). Id of the contact.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> contact = redmine.helpdesk_contact.get(1)
   >>> contact.email
   'jane@example.com'

all
+++

Not supported by the Helpdesk plugin

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns HelpdeskContact resources that match the given lookup parameters, sorted by name and email.

   :param project_id: (required). Id or identifier of contacts' project.
   :type project_id: int or string
   :param string email: (optional). Exact, case-insensitive email match, takes precedence over ``search``.
   :param string search: (optional). Substring search over name, email and company.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> contacts = redmine.helpdesk_contact.filter(project_id='support', search='acme')
   >>> contacts
   <redminelib.resultsets.ResourceSet object with HelpdeskContact resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a HelpdeskContact resource and saves them to the Helpdesk plugin.
   Accepts the same fields as ``create()`` except ``project_id`` and ``email``, which can't be changed.

   :param int resource_id: (required). Contact id.
   :return: True

.. code-block:: python

   >>> redmine.helpdesk_contact.update(1, phone='+49 123 456')
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.HelpdeskContact
   :noindex:

   Saves current state of a HelpdeskContact resource to the Helpdesk plugin.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> contact = redmine.helpdesk_contact.get(1)
   >>> contact.save(company='ACME Corp')
   <redminelib.resources.HelpdeskContact #1 "Jane Doe">

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single HelpdeskContact resource from the Helpdesk plugin by its id.

   :param int resource_id: (required). Contact id.
   :return: True

.. code-block:: python

   >>> redmine.helpdesk_contact.delete(1)
   True

Export
------

Not supported by the Helpdesk plugin
