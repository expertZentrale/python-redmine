Expert Agile Data
=================

.. versionadded:: 3.0.0

Requires Redmine >= 5.0 and the ``redmine_expert_agile`` plugin >= 0.6.0. Reading requires the
``view_expert_agile_board`` permission, updating requires ``edit_expert_agile_board`` and ``edit_issues``,
changing the sprint additionally requires ``manage_expert_agile_backlog``.

Agile data holds story points, sprint and board position of a single issue. It exists for every issue
and is addressed by the issue id.

Manager
-------

All operations on the ExpertAgileData resource are provided by its manager. To get access to it
you have to call ``redmine.expert_agile_data`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by the Agile plugin, use ``update()``.

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns agile data of an issue. Attributes are None if nothing was set yet.

   :param int resource_id: (required). Id of the issue.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> data = redmine.expert_agile_data.get(42)
   >>> data
   <redminelib.resources.ExpertAgileData #42>
   >>> data.story_points, data.sprint_id, data.position
   (5, 3, '1024.0')
   >>> data.issue
   <redminelib.resources.Issue #42 "Printer on fire">

all
+++

Not supported by the Agile plugin

filter
++++++

Not supported by the Agile plugin

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates agile data of an issue, omitted fields are left unchanged. The change is journaled on the issue.

   :param int resource_id: (required). Id of the issue.
   :param int story_points: (optional). Story points, None clears them.
   :param int sprint_id: (optional). Id of an open sprint available in the issue's project, None clears it.
   :return: True

.. code-block:: python

   >>> redmine.expert_agile_data.update(42, story_points=8, sprint_id=3)
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.ExpertAgileData
   :noindex:

   Saves current state of the agile data. ``position`` is read-only.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> data = redmine.expert_agile_data.get(42)
   >>> data.save(story_points=3)
   <redminelib.resources.ExpertAgileData #42>

.. hint::

   Agile data can also be set when creating or updating an issue (creating requires plugin >= 0.6.1,
   older versions reject it with "Issue cannot be blank"):

   .. code-block:: python

      >>> redmine.issue.create(
      ...     project_id='scrum',
      ...     subject='New story',
      ...     expert_agile_data_attributes={'story_points': 5, 'sprint_id': 3}
      ... )

Delete methods
--------------

Not supported by the Agile plugin

Export
------

Not supported by the Agile plugin
