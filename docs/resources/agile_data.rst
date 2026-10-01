Agile Data
==========

.. versionadded:: 3.1.0

Requires the RedmineUP `Agile plugin <https://www.redmineup.com/pages/plugins/agile>`_ (``redmine_agile``)
>= 1.6.0 and the ``view_agile_queries`` permission.

Agile data holds story points, sprint, board position and color of a single issue. It is read-only, the plugin
takes changes through the issue (see below).

.. note::

   This resource targets RedmineUP's Agile plugin. For ``redmine_expert_agile`` see :doc:`expert_agile_data`.

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns agile data of an issue, attributes are None if nothing was set yet.

   :param int resource_id: (required). Id of the issue.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> data = redmine.agile_data.get(42)
   >>> data
   <redminelib.resources.AgileData #42>
   >>> data.story_points, data.agile_sprint_id, data.position
   (3, 5, 2)
   >>> data.issue
   <redminelib.resources.Issue #42 "Foo">

Changing agile data
-------------------

Story points and sprint are set through the issue with ``agile_data_attributes``. ``agile_sprint_id`` is
silently dropped by the plugin without the ``manage_sprints`` permission:

.. code-block:: python

   >>> redmine.issue.update(42, agile_data_attributes={'story_points': 5, 'agile_sprint_id': 5})
   True

Issues of a sprint can be found with the ``agile_sprints`` issue filter:

.. code-block:: python

   >>> redmine.issue.filter(project_id='scrum', agile_sprints=5)
