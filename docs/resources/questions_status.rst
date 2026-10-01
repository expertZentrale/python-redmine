Questions Status
================

.. versionadded:: 3.1.0

Requires the RedmineUP `Questions plugin <https://www.redmineup.com/pages/plugins/questions>`_
(``redmine_questions``) >= 1.0.0.

The question statuses are the only part of the Questions plugin that can be used with an API key, questions,
answers and sections are not available through its REST API.

Read methods
------------

all
+++

.. py:method:: all()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all QuestionsStatus resources.

   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> statuses = redmine.questions_status.all()
   >>> [(s.name, s.is_closed) for s in statuses]
   [('Open', False), ('Solved', True)]

.. hint::

   ``get(id)`` works too, it picks the status from ``all()``.
