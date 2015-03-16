
======
Tables
======

ModelTable
----------

`tables.py`

.. code-block:: python

    from horizon_contrib.tables.base import ModelTable

    from .models import MyModelClass

    class MyModelTable(ModelTable):

        class Meta:

            model_class = MyModelClass
            
            # or as string, but this makes some additional db queries
            model_class = "mymodelclass"


and then `views.py`

.. code-block:: python

    from horizon_contrib.tables.views import IndexView

    from .tables import MyModelTable

    class IndexView(BaseIndexView):
        table_class = MyModelTable
        template_name = 'myapp/mymodel/index.html' # or leave blank

.. note:: 

    for easy table inheritence we supports ``model_class`` directly on the table class

.. code-block:: python

    ...
    
    class MyModelTable(ModelTable):

        model_class = MyModelClass
    
    ...


Specifing columns and ordering
------------------------------

.. code-block:: python

    from horizon_contrib.tables import ModelTable

    class MyModelTable(ModelTable):

        class Meta:
            columns = ("project", "issue", ..)
            order_by = ("id") # queryset.order_by(self._meta.order_by)

.. note::

    order by is used for generic queryset for more customization override ``get_table_data``

Custom columns
--------------

.. code-block:: python

    from horizon import tables
    from horizon_contrib.tables import ModelTable

    class MyModelTable(ModelTable):

        project = tables.Column('project', ..)

        class Meta:
            extra_columns = True # generates other columns within ``project``
            # default is False

.. note::

    In the default state if we specified one column no other columns will be generated for this purpose set ``extra_columns = True``

Load Data into Table
--------------------

.. note::

    This is main change against Horizon, but old way is still supported and it's only about overriding ``get_data`` on the DataTable View.

With Django model simply do this

.. code-block:: python

    class MyModelTable(ModelTable):

        def get_table_data(self):
            return self._model_class.objects.all().order_by("status__id")

PaginatedTable
--------------

`tables.py`

.. code-block:: python

    from horizon_contrib.tables.base import PaginatedTable

    class MyModelTable(PaginatedTable):


        class Meta:
        
            model_class = MyModelClass

and then `views.py`

.. code-block:: python

    from horizon_contrib.tables.views import PaginatedView

    from .tables import MyModelTable

    class IndexView(IndexView):
        table_class = MyModelTable


PaginatedModelTable
-------------------

this table combine ModelTable and Pagination

.. code-block:: python

    from horizon_contrib.tables import PaginatedModelTable

    class MyModelTable(PaginatedModelTable):

        model_class = "mymodelclass"


and then `views.py`

.. code-block:: python

    from horizon_contrib.tables.views import PaginatedView

    from .tables import PaginatedModelTable

    class IndexView(IndexView):
        table_class = PaginatedModelTable


Inheritance of the 'Meta' class
-------------------------------

.. code-block:: python

    from horizon_contrib.tables import ModelTable

    class IssueTable(ModelTable):

        subject = tables.Column('subject')

        class Meta:

            model_class = "mymodelclass"
            extra_columns = True

    class UserIssueTable(ModelTable):

        class Meta(IssueTable.Meta):

            extra_columns = False