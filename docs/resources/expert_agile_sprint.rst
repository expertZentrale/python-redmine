Expert Agile Sprint
===================

.. versionadded:: 3.0.0

Requires Redmine >= 5.0 and the ``redmine_expert_agile`` plugin >= 0.6.0. All operations, including
read ones, require the ``manage_expert_agile_sprints`` permission and the Agile module enabled in the project.

.. note::

   This resource targets ``redmine_expert_agile`` and is not compatible with RedmineUP's Agile plugin,
   which uses different endpoints and payloads.

Manager
-------

All operations on the ExpertAgileSprint resource are provided by its manager. To get access to it
you have to call ``redmine.expert_agile_sprint`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Sprints are always addressed through their project, so every manager method needs a ``project_id``.
Resource methods (``save()``, ``delete()``, ``refresh()``) use the sprint's own project automatically.
A sprint shared into another project can only be read through the project owning it.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new ExpertAgileSprint resource with given fields.

   :param project_id: (required). Id or identifier of sprint's project.
   :type project_id: int or string
   :param string name: (required). Sprint name, unique per project.
   :param start_date: (required). Sprint start date.
   :type start_date: string or date object
   :param end_date: (required). Sprint end date, on or after the start date.
   :type end_date: string or date object
   :param string description: (optional). Sprint description.
   :param string status:
    .. raw:: html

       (optional). Status of the sprint, one of:

    - open (default)
    - active (the previously active sprint of the project is reopened)
    - closed (refused while the sprint still has open issues)

   :param string sharing:
    .. raw:: html

       (optional). Sprint sharing, one of:

    - none (default)
    - descendants
    - hierarchy
    - tree
    - system (admin only)

   :return: :ref:`Resource` object

.. note::

   The plugin expects ``status`` and ``sharing`` as integers but returns them as names, Python-Redmine
   converts the names listed above automatically so you can always work with names.

.. code-block:: python

   >>> sprint = redmine.expert_agile_sprint.create(
   ...     project_id='scrum',
   ...     name='Sprint 3',
   ...     start_date=datetime.date(2026, 1, 5),
   ...     end_date=datetime.date(2026, 1, 16),
   ...     status='open'
   ... )
   >>> sprint
   <redminelib.resources.ExpertAgileSprint #3 "Sprint 3">

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty ExpertAgileSprint resource but saves it only when ``save()`` is called. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single ExpertAgileSprint resource by its id, including ``issue_count`` and ``story_points``
   of the issues visible to the user.

   :param int resource_id: (required). Id of the sprint.
   :param project_id: (required). Id or identifier of sprint's project.
   :type project_id: int or string
   :return: :ref:`Resource` object

.. code-block:: python

   >>> sprint = redmine.expert_agile_sprint.get(3, project_id='scrum')
   >>> sprint.status, sprint.story_points
   ('active', 13)

all
+++

Not supported by the Agile plugin

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all ExpertAgileSprint resources of a project, active first, then open, then closed. The plugin
   doesn't paginate, ``limit`` and ``offset`` are applied by Python-Redmine.

   :param project_id: (required). Id or identifier of sprints' project.
   :type project_id: int or string
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> sprints = redmine.expert_agile_sprint.filter(project_id='scrum')
   >>> sprints
   <redminelib.resultsets.ResourceSet object with ExpertAgileSprint resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of an ExpertAgileSprint resource. Accepts the same fields as ``create()``.

   :param int resource_id: (required). Sprint id.
   :param project_id: (required). Id or identifier of sprint's project.
   :type project_id: int or string
   :return: True

.. code-block:: python

   >>> redmine.expert_agile_sprint.update(3, project_id='scrum', end_date=datetime.date(2026, 1, 20))
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.ExpertAgileSprint
   :noindex:

   Saves current state of an ExpertAgileSprint resource.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> sprint = redmine.expert_agile_sprint.get(3, project_id='scrum')
   >>> sprint.save(name='Sprint 3 (extended)')
   <redminelib.resources.ExpertAgileSprint #3 "Sprint 3 (extended)">

There are also ``activate()`` and ``close()`` shortcuts which set the status and save the sprint:

.. code-block:: python

   >>> sprint.close()
   <redminelib.resources.ExpertAgileSprint #3 "Sprint 3 (extended)">

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes an ExpertAgileSprint, its issues are unassigned from the sprint. Refused while issues of
   other projects are still in the sprint.

   :param int resource_id: (required). Sprint id.
   :param project_id: (required). Id or identifier of sprint's project.
   :type project_id: int or string
   :return: True

.. code-block:: python

   >>> redmine.expert_agile_sprint.delete(3, project_id='scrum')
   True

Export
------

Not supported by the Agile plugin
