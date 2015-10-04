
|PypiVersion| |Doc badge| |Pypi|

======================
horizon-django contrib
======================

.. contents::
   :local:

Library built on top of Django and Horizon(part of OpenStack Dashboard) for building modern web applications.

*With this toolkit is building applications blazingly fast and easy !*

This library provide generic implementation most of Horizon components, add more tools for easily scaffolding applications and preserves support for complex customizations.

Short story
-----------

Horizon is pretty package for fast creating UI for everything. But is designed for model-less applications like an OpenStack Dashboard.
If we connect Horizon with typical Django application we must create same pieces of same components and this is really suck !
We want more declarative and less imperative code. For this purpose we create this library which compose common stuff in one place.

Features
--------

- With Django and Conent Types

    - Views - PaginatedIndex, Create, Update, Delete in Angular modal's
    - Tables with inline-ajax update
    - Modal Forms autohandled
    - Generic - IndexView with pagination, CRUD actions and AJAX inline-edit.

no implementation required, all Django stuff is generated automatically like an admin, but in more customizeable and extendable form.

- Rest API Dashboards

    - APIModel
    - Manager
    - ClientBase - simple implementation which uses ``requests``
    - Generic - Tables, Views, Actions

and plus all features defined under Django because if we have model most of things works well without any modification.

Manager has all responsibilty for get data from remote API. It`s simple object which has similar methods with django model managers. And it's bound to Abstract model.

- Others

    - ReactJS integration - for large tables with thousands rows we have integrated https://github.com/glittershark/reactable as ``ReactTable``
    - LinkedListColumn
    - set of common filters, templatetags

See [Documentation]_ !
`Examle App <https://github.com/michaelkuty/horizon-sensu-panel>`_

Requires
--------

* Django
* Horizon - part of OpenStack Dashboard

Tested with
-----------

* Horizon 2012+ (Icehouse +)
* Django 1.4 +
* Python 2.6 +

Installation
------------

.. code-block:: bash

    pip install horizon-contrib

    pip install git+https://github.com/michaelkuty/horizon-contrib.git@develop

Now as you wish install horizon, if you don't know about this, use this command::

    pip install horizon-contrib[horizon]

Configuration
-------------

.. code-block:: python

    INSTALLED_APPS += ('horizon_contrib',)

Next configuration depends on your scenario

For usually Django application we must include ``horizon_contrib.urls`` or include ``horizon.urls``. If we include horizon's urls Contrib urls will be mapped as Horizon dashboard. 

.. code-block:: python

    from django.conf.urls import patterns, include, url

    urlpatterns = patterns('',
        ...
        url(r'^contrib/', include('horizon_contrib.urls'), ),
        ...
        # or
        url(r'^horizon/', include('horizon.urls'), ),
    )

Django example
--------------

With Django model everythings works well without any code. Only navigate your browser to 

* ``/contrib/models/project/index``
* ``/contrib/models/project/create``
* ``/contrib/models/project/1/update``

For override behaviour see doc.


Horizon example REST-API !
--------------------------

Dashboard structure::

    my_dashboard
        |-- __init__.py
        |-- projects
            |-- __init__.py
            |-- models.py   # define data structure
            |-- managers.py # load remote data
            |-- panel.py    # register namespace
        |-- dashboard.py

Your ``models.py``

.. code-block:: python

    from horizon_contrib.api import APIModel
    from horizon_contrib.common import register_model

    class Project(APIModel):

        name = models.CharField('id', primary_key=True)  # default primary is id
        description = models.CharField..
        ...

        objects = Manager()  # see below

        class Meta:
            verbose_name = 'Project'
            abstract = True

    register_model(Project)  # supply Django Content Type framework

New ``managers.py``

.. code-block:: python

    from horizon_contrib.api import Manager

    class Manager(Manager):

        def all(self, *args, **kwargs):
            return self.request('/projects')

Finally ``panel.py``

.. code-block:: python

    from horizon_contrib.panel import ModelPanel
    from horizon_redmine.dashboard import RedmineDashboard

    class ProjectPanel(ModelPanel):
        name = "Projects"
        slug = 'projects'
        model_class = 'project'

    RedmineDashboard.register(ProjectPanel)

navigate your browser to 

* ``/contrib/models/project/index``
* ``/contrib/models/project/create``
* ``/contrib/models/project/1/update`` 

For React SortTable

.. code-block:: bash

    pip install xstatic-react

Add to ``settings.py``

.. code-block:: python

    import xstatic.pkg.react

    STATICFILES_DIRS = [
        ('lib', xstatic.main.XStatic(xstatic.pkg.react).base_dir),

    ]

* ``/contrib/models/project/react`` ..

.. code-block:: python

    from horizon_contrib.tables import ReactTable

For more code see [Documentation]_.

Read more
---------

* http://horizon-contrib.readthedocs.org
* https://www.djangoproject.com/
* https://github.com/openstack/horizon
* http://docs.openstack.org/developer/horizon/

.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat
.. |Doc badge| image:: https://readthedocs.org/projects/horizon-contrib/badge/?version=stable
.. |Pypi| image:: https://img.shields.io/pypi/dm/horizon-contrib.svg
.. |PypiVersion| image:: https://badge.fury.io/py/horizon-contrib.svg
.. [Documentation] http://horizon-contrib.readthedocs.org
