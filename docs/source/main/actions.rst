
=======
Actions
=======

Horizon has two types of actions

* TableActions
* RowActions

some actions can by used for both categories.

Filter Action
-------------

Simple filter action which provide initial for our ``client-side`` filtering. Server-side is not implemented for now, but is not too many work and it's in the plan. 

default search in all fields

.. code-block:: python

    from horizon_contrib.tables.actions import FilterAction

or specify one field

.. code-block:: python

    from horizon_contrib.tables.actions import FilterAction

    class MyFilter(FilterAction):

        fields = ['name', 'subject']

        lookups = ['project__name']

DeleteAction
------------

Simple action based on horizon's ``DeleteAction``. It's ``BatchAction`` for more detail see Horizon doc.

.. code-block:: python

    from horizon import tables
    from horizon_contrib.tables import DeleteAction

    class MyTable(tables.DataTable):

        class Meta:
            table_actions = (DeleteAction,)
            row_actions = (DeleteAction,)

.. warning::

    For this time is not implemented in transaction !

CreateAction
------------

There is nothing special it's only ``LinkAction`` with implemented ``get_link_url``

.. code-block:: python

    from horizon_contrib.tables.actions import CreateAction

UpdateAction
------------

There is nothing special it's only ``LinkAction`` with implemented ``get_link_url``

.. code-block:: python

    from horizon_contrib.tables.actions import UpdateAction

.. note::

    for more details and customization follow ``UpdateView``

Packs of Actions
----------------

For less code is there some action packs

* ``CD_ACTIONS`` - ``CREATE`` and ``DELETE`` can be used for table and row actions
* ``ROW_ACTIONS`` - same as CD_ACTIONS, but with UpdateAction
* ``TABLE_ACTIONS`` - same as CD_ACTIONS but with FilterAction

.. code-block:: python

    from horizon import tables
    from horizon_contrib.tables import ROW_ACTIONS, TABLE_ACTIONS

    class MyTable(tables.DataTable)

        class Meta:
            row_actions = ROW_ACTIONS
            tables_actions = TABLE_ACTIONS

.. warning::

    In default state these actions sets works only with our table classes !

UpdateColumnAction
------------------

This action is used for column as additional attribute and provide Ajax update power.

Optionaly can be provided form ``field`` with ``widget``.

.. code-block:: python

    from horizon import tables
    from horizon_contrib.tables.actions import UpdateAction

    my_column = tables.Columns('my_column', update_action=UpdateAction)