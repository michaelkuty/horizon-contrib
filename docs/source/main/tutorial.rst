
==============
Short tutorial
==============

Include our urls.

.. code-block:: python


    from django.conf.urls import patterns, include, url

    urlpatterns = patterns('',
        ...
        url(r'^contrib/', include('horizon_contrib.urls', namespace='horizon_contrib'), ),
        ...
    )

Visit these urls

.. code-block:: python

    /contrib/models/<model_name>/index/
    /contrib/models/<model_name>/create/
    /contrib/models/<model_name>/<model_id>/update/

.. note::

	For these purpose must be ``django.contrib.contenttypes`` in ``INSTALLED_APPS``.