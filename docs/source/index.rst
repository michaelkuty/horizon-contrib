
======================
horizon-django contrib
======================

|PypiVersion| |License badge| |Doc badge| |Pypi|

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
    - ClientBase - simple implementation which uses ``requests``
    - Generic - Tables, Views, Actions

and plus all features defined under Django because if we have model most of things works well without any modification.

Manager has all responsibilty for get data from remote API. It`s simple object which has similar methods with django model managers. And it's bound to Abstract model.

- Others

    - ReactJS integration - for large tables with thousands rows we have integrated https://github.com/glittershark/reactable as ``ReactTable``
    - tabs, templates (modal login, ...)
    - set of common filters, templatetags

`Examle App <https://github.com/michaelkuty/horizon-sensu-panel>`_

Contents:

.. toctree::
   :maxdepth: 2

   main/tutorial
   main/generic
   main/api
   main/tables
   main/forms
   main/actions
   main/reactjs
   main/filters

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

Optionaly include ``horizon_contrib.urls`` with ``namespace='horizon'``. This is only for generic functionality like a index,create,update,delete views.

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

With Django model everythings works well without any code. Only navigate your browser to 

* ``/contrib/models/project/index``
* ``/contrib/models/project/create``
* ``/contrib/models/project/1/update``

For override behaviour see doc.

.. note::

    ``project`` in url is model name

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

navigate your browser to ``/contrib/models/project/index`` ! or ``/contrib/models/project/create``


.. warning::

    This project depends on Horizon library, but isn't in the requirements ! You may use ``leonardo-horizon`` or openstack horizon.


Read more
---------

* http://horizon-contrib.readthedocs.org
* https://www.djangoproject.com/
* https://github.com/openstack/horizon
* http://docs.openstack.org/developer/horizon/

.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat
.. |Doc badge| image:: https://readthedocs.org/projects/horizon-contrib/badge/?version=stable
.. |Donation| image:: http://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif
.. |Pypi| image:: https://pypip.in/d/horizon-contrib/badge.svg?style=flat
.. |PypiVersion| image:: https://pypip.in/version/horizon-contrib/badge.svg?style=flat

.. _Donation: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZYP3NZCQWF5CN


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`