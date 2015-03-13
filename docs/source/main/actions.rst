
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


UpdateAction
------------

Ajax update power !

.. code-block:: python

	from horizon import tables
    from horizon_contrib.tables.actions import UpdateAction

    my_column = tables.Columns('my_column', update_action=UpdateAction)