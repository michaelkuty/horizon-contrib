
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

no implementation required, all Django stuff is generated automatically like an admin, but in more customizeable and extendable form.

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

Configuration
-------------

.. code-block:: python

    INSTALLED_APPS += ('horizon_contrib',)

Optionaly include ``horizon_contrib.urls`` with ``namespace='horizon_contrib'``. This is only for generic functionality like a index,create,update,delete views.

.. code-block:: python

    from django.conf.urls import patterns, include, url

    urlpatterns = patterns('',
        ...
        url(r'^contrib/', include('horizon_contrib.urls', namespace='horizon'), ),
        ...
    )

.. note::

    ``namespace`` is important for url ``reverse``

Django example
--------------

*Your* models.py

.. code-block:: python

    from django import models

    class Project(models.Model):

        name = models.CharField..
        description = models.CharField..
        ...

        class Meta:
            verbose_name = 'Project'

navigate your browser to ``/contrib/models/project/index`` !
or ``/contrib/models/project/create``

Horizon example REST-API !
--------------------------

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

navigate your browser to ``/contrib/models/project/index`` ! or ``/contrib/models/project/create``

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