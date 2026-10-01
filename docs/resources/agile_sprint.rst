Agile Sprint
============

.. versionadded:: 3.1.0

Requires the RedmineUP `Agile plugin <https://www.redmineup.com/pages/plugins/agile>`_ (``redmine_agile``) PRO
>= 1.6.0, sprints have to be enabled in its settings. Listing, creating, updating and deleting require the
``manage_sprints`` permission, reading a single sprint requires ``manage_backlog``.

.. note::

   This resource targets RedmineUP's Agile plugin. For ``redmine_expert_agile`` see :doc:`expert_agile_sprint`.

Manager
-------

All operations on the AgileSprint resource are provided by its manager. To get access to it you have to call
``redmine.agile_sprint`` where ``redmine`` is a configured redmine object. Sprints are always addressed through
their project, resource methods (``save()``, ``delete()``, ``refresh()``) use the sprint's project automatically.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new AgileSprint resource with given fields.

   :param project_id: (required). Id or identifier of sprint's project.
   :type project_id: int or string
   :param string name: (required). Sprint name, unique per project.
   :param start_date: (required). Sprint start date.
   :type start_date: string or date object
   :param end_date: (required). Sprint end date.
   :type end_date: string or date object
   :param string description: (optional). Sprint description.
   :param string status: (optional). One of ``open`` (default), ``active`` or ``closed``, converted to the
    integer the plugin expects.
   :param string sharing: (optional). One of ``none`` (default), ``descendants``, ``hierarchy``, ``tree`` or
    ``system``, converted to the integer the plugin expects.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> sprint = redmine.agile_sprint.create(
   ...     project_id='scrum',
   ...     name='Sprint 5',
   ...     start_date=datetime.date(2026, 1, 5),
   ...     end_date=datetime.date(2026, 1, 16),
   ...     status='active'
   ... )
   >>> sprint
   <redminelib.resources.AgileSprint #5 "Sprint 5">

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single AgileSprint resource with ``story_points``, ``done_ratio`` and (with the
   ``view_time_entries`` permission) ``estimated_hours`` and ``spent_hours`` of its issues. The plugin
   doesn't return dates, status and sharing here, use ``filter()`` for the dates.

   :param int resource_id: (required). Id of the sprint.
   :param project_id: (required). Id or identifier of sprint's project.
   :type project_id: int or string
   :param list include:
    .. raw:: html

       (optional). Fetches associated data in one call. Accepted values:

    - issues

   :return: :ref:`Resource` object

.. code-block:: python

   >>> sprint = redmine.agile_sprint.get(5, project_id='scrum', include=['issues'])
   >>> sprint.story_points
   13
   >>> sprint.issues
   <redminelib.resultsets.ResourceSet object with Issue resources>

.. warning::

   In a live test with Agile 1.6.14 the plugin returned ``story_points`` and ``estimated_hours`` of the sprint's
   issues as null (and the sprint total as 0) although the issues had them. Read story points per issue from
   :doc:`agile_data` instead of relying on the sprint totals.

all
+++

Not supported by the Agile plugin

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns the project's own AgileSprint resources (shared sprints aren't listed) with name, description and
   dates. The plugin doesn't paginate.

   :param project_id: (required). Id or identifier of sprints' project.
   :type project_id: int or string
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> sprints = redmine.agile_sprint.filter(project_id='scrum')
   >>> sprints
   <redminelib.resultsets.ResourceSet object with AgileSprint resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of an AgileSprint resource. Accepts the same fields as ``create()``.
   The plugin answers with a redirect to the sprint's HTML page, which is not followed but treated as success.

   :param int resource_id: (required). Sprint id.
   :param project_id: (required). Id or identifier of sprint's project.
   :type project_id: int or string
   :return: True

.. code-block:: python

   >>> redmine.agile_sprint.update(5, project_id='scrum', status='closed')
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.AgileSprint
   :noindex:

   Saves current state of an AgileSprint resource.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> sprint = redmine.agile_sprint.filter(project_id='scrum')[0]
   >>> sprint.save(end_date=datetime.date(2026, 1, 20))
   <redminelib.resources.AgileSprint #5 "Sprint 5">

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes an AgileSprint, its issues are unassigned from it.

   :param int resource_id: (required). Sprint id.
   :param project_id: (required). Id or identifier of sprint's project.
   :type project_id: int or string
   :return: True

.. code-block:: python

   >>> redmine.agile_sprint.delete(5, project_id='scrum')
   True

Export
------

Not supported by the Agile plugin
