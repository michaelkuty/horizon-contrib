
=============
Table Actions
=============

Filter Action
-------------

default search in all fields

.. code-block:: python

    from horizon_contrib.tables.actions import FilterAction


or specify one field

.. code-block:: python

    from horizon_contrib.tables.actions import FilterAction

    class MyFilter(FilterAction):

        fields = ['name', 'subject']

        lookups = ['project__name']
