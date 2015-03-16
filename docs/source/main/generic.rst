
==============
Generic module
==============

This module can be used for good examplanation what is happening in generic views.

views.py
--------

.. code-block:: python

    from horizon_contrib import tables


    class GenericTable(tables.ModelTable):

        def get_object_display(self, datum):
            return datum.__unicode__()

        def get_object_id(self, datum):
            return datum.pk

        class Meta:

            table_actions = tables.TABLE_ACTIONS
            row_actions = tables.ROW_ACTIONS
            extra_columns = True

views.py
--------

.. code-block:: python

    from horizon_contrib import tables
    from horizon_contrib.common import get_class

    from .tables import GenericTable


    class GenericIndexView(tables.PaginatedView):

        """contruct table from model class
        """

        table_class = GenericTable

        def get_data(self):
            try:
                # this is the magic stuff, move responsibility for get data to table.
                # table has connection to model and model has own manager for get right data
                # table has request and all his stuff like an arguments etc..
                objects = self.get_table().get_table_data()
            except Exception, e:
                raise e
            return objects

urls.py
--------

.. code-block:: python

    from django.conf.urls import patterns, url
    from horizon_contrib.forms.views import CreateView, UpdateView

    from .views import GenericIndexView

    urlpatterns = patterns('',
        url(r'^model/(?P<cls_name>[\w\.\-]+)/create/$', CreateView.as_view(), name='create'),
        url(r'^model/(?P<cls_name>[\w\.\-]+)/(?P<id>[\w\.\-]+)/update/$', UpdateView.as_view(), name='update'),
        url(r'^model/(?P<cls_name>[\w\.\-]+)/index/$', GenericIndexView.as_view(), name='index'),
    )

.. note::

    Maybe we cant't see here how we propagate model_class into table. It's provided as cls_name in kwargs as we see in urls.py


.. warning::

	For these purpose must be ``django.contrib.contenttypes`` in ``INSTALLED_APPS``.