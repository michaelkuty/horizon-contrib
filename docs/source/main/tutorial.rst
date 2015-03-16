
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

With Horizon is same urls and its autodicovered in default state. But if we have our urls patterns we must respect ordering for including urls.

.. code-block:: python

    from django.conf import settings
    from django.conf.urls import include  # noqa
    from django.conf.urls import patterns
    from django.conf.urls.static import static  # noqa
    from django.conf.urls import url
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # noqa

    import horizon

    urlpatterns = patterns('',
        url(r'^$', 'openstack_dashboard.views.splash', name='splash'),
        url(r'^auth/', include('openstack_auth.urls')),
        url(r'', include(horizon.urls)),
        url(r'^contrib/', include('horizon_contrib.urls', namespace='horizon'), ),  # must be under horizon !
    )


.. note::

	For these purpose must be ``django.contrib.contenttypes`` in ``INSTALLED_APPS``.