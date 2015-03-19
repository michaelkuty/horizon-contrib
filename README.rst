
|PypiVersion| |License badge| |Doc badge| |Pypi|

======================
horizon-django contrib
======================

Library built on top of Django and Horizon(part of OpenStack Dashboard) for building modern web applications.

*With this toolkit is building applications blazingly fast and easy !*

This library provide generic implementation most of Horizon components, add more tools for easily scaffolding applications and preserves support for complex customizations.

Short story
-----------

Horizon is pretty package for fast creating UI for everything. But is designed for model-less applications like an OpenStack Dashboard.
If we connect Horizon with typical Django application we must create same pieces of same components and this is realy suck !
We want more declarative and less imperative code. For this purpose we create this library which compose common stuff in one place.

Features
--------

- With Django and Conent Types

    - Views - PaginatedIndex, Create, Update, Delete in Angular modal's
    - Tables with inline-ajax update
    - Modal Forms with autohandled modelforms

no implementation required, all Django stuff is generated automatically like an admin, but in more customizeable form.

*Required*

Model -> Panel

*Usual*

Model -> Panel -> Table -> bound actions(CRUD with Filter) -> View -> Pagination

- Rest API Dashboards

    - APIModel
    - ClientBase - simple implementation which uses ``requests``

and plus all features defined under Django because if we have model most of things works well without any modification.

*Required*

Model -> Panel

*Usual*

Manager -> Model -> Panel -> Table -> bound actions(CRUD with Filter) -> View -> Pagination

Manager has all responsibilty for get data from remote API. It`s simple object which has similar methods with django model managers. And it's bound to Abstract model.

- Others

    - ReactJS integration - for large tables with thousands rows we have integrated https://github.com/glittershark/reactable as ``ReactTable``
    - tabs, templates (modal login, ...)
    - set of common filters, templatetags

See [Documentation]_ !

Requires
--------

* Horizon - part of OpenStack Dashboard

Tested with
-----------

* Horizon Icehouse, Juno, Kilo
* Django 1.5 .. 1.8
* Python 2.6 .. 3.4

Installation
------------

This project depends on Horizon library, but isn't installed automatically !

If you haven't installed Horizon, do something like this in your ``virtualenv``:

.. code-block:: bash

    (env)majklk@horizon:~# pip install horizon-contrib

    (env)majklk@horizon:~# pip install git+https://github.com/michaelkuty/horizon-contrib.git@develop

or clone and add to ``$PYTHONPATH``.

Configuration
-------------

.. code-block:: python

    INSTALLED_APPS += ('horizon_contrib',)

    url(r'^contrib/', include('horizon_contrib.urls', namespace='horizon'), ),

If used horizon, contrib urls will be included automatically.

Manually include ``horizon_contrib.urls`` with ``namespace='horizon'`` is simple.

.. code-block:: python

    from django.conf.urls import patterns, include, url

    urlpatterns = patterns('',
        ...
        url(r'^contrib/', include('horizon_contrib.urls', namespace='horizon'), ),
        ...
    )

.. note::

    If we include horizon urls contrib must be below horizon urls !

For more code see [Documentation]_.

Read more
---------

* http://horizon-contrib.readthedocs.org
* https://www.djangoproject.com/
* https://github.com/openstack/horizon
* http://docs.openstack.org/developer/horizon/

.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat
.. |Doc badge| image:: https://readthedocs.org/projects/horizon-contrib/badge/?version=stable
.. |Pypi| image:: https://pypip.in/d/horizon-contrib/badge.svg?style=flat
.. |PypiVersion| image:: https://pypip.in/version/horizon-contrib/badge.svg?style=flat
.. [Documentation] http://horizon-contrib.readthedocs.org