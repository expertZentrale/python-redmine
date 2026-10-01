Helpdesk Project Setting
========================

.. versionadded:: 3.0.0

Requires Redmine >= 5.0 and the ``redmine_expert_helpdesk`` plugin >= 0.20.0. Reading requires the
``view_helpdesk_info`` or ``manage_helpdesk`` permission, updating requires ``manage_helpdesk``.

Helpdesk settings exist exactly once per project, hence the resource is addressed by its project.

Manager
-------

All operations on the HelpdeskProjectSetting resource are provided by its manager. To get access to it
you have to call ``redmine.helpdesk_project_setting`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by the Helpdesk plugin

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns helpdesk settings of a project.

   :param resource_id: (required). Id or identifier of the project.
   :type resource_id: int or string
   :return: :ref:`Resource` object

.. code-block:: python

   >>> setting = redmine.helpdesk_project_setting.get('support')
   >>> setting.project_id
   1
   >>> setting.sla_work_days
   '1,2,3,4,5'
   >>> setting.sla_priorities
   [{'priority_id': 2, 'priority_name': 'Normal', 'reaction_minutes': 60, 'solution_minutes': 480}]

all
+++

Not supported by the Helpdesk plugin

filter
++++++

Not supported by the Helpdesk plugin

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Partially updates helpdesk settings of a project, only given fields are changed. See the plugin's
   ``API.md`` for the complete list of fields.

   :param resource_id: (required). Id or identifier of the project.
   :type resource_id: int or string
   :param list sla_priorities: (optional). Per priority SLA overrides as a list of dicts with
    ``priority_id``, ``reaction_minutes`` and ``solution_minutes`` keys, an override with both minutes
    set to None is removed.
   :return: :ref:`Resource` object with the updated settings

.. code-block:: python

   >>> redmine.helpdesk_project_setting.update(
   ...     'support',
   ...     sla_enabled=True,
   ...     sla_reaction_minutes=120,
   ...     sla_priorities=[{'priority_id': 4, 'reaction_minutes': 30, 'solution_minutes': 240}]
   ... )
   <redminelib.resources.HelpdeskProjectSetting #1>

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.HelpdeskProjectSetting
   :noindex:

   Saves current state of the settings.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> setting = redmine.helpdesk_project_setting.get('support')
   >>> setting.save(phishing_check_enabled=True, phishing_action='quarantine')
   <redminelib.resources.HelpdeskProjectSetting #1>

Delete methods
--------------

Not supported by the Helpdesk plugin

Export
------

Not supported by the Helpdesk plugin
