
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
If we connect Horizon with typical Django application we must create same pieces of same components and this is realy suck !
We want more declarative and less imperative code. For this purpose we create this library which compose common stuff in one place.

Features
--------

- With Django and Conent Types

    - Views - PaginatedIndex, Create, Update, Delete on client side with AngularJS, D3.js, Bootstrap3, ..
    - Tables with inline-ajax update
    - Actions - Filter, Create, Update, Delete

no implementation required, all Django stuff is generated automatically like an admin, but in more customizeable form.

Model -> Form -> Table -> bound actions(CRUD with Filter) -> View -> Pagination

- Rest API Dashboards

    - APIModel
    - ClientBase - simple implementation which uses ``requests``

and plus all features defined under Django, because if we have model most of things works well without any modification.

Manager -> Model -> Form -> Table -> bound actions(CRUD with Filter) -> View -> Pagination

Manager has all responsibilty for get data from remote API. It`s simple object which has similar methods with django model managers. And it's bound to Abstract model.

- Others

    - tabs, templates (modal login, ...)
    - set of common filters, templatetags

Contents:

.. toctree::
   :maxdepth: 2

   main/tutorial
   main/tables
   main/api
   main/generic
   main/forms
   main/actions
   main/filters

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
        url(r'^contrib/', include('horizon_contrib.urls', namespace='horizon_contrib'), ),
        ...
    )

.. note::

    ``namespace`` is important for url ``reverse``

Show me the code !
------------------

*Your* models.py

.. code-block:: python

    from django import models

    class Project(models.Model):

        name = models.CharField..
        description = models.CharField..

*New* tables.py

.. code-block:: python

    from horizon_contrib.tables import ModelTable
    from .models import Project

    class ProjectTable(ModelTable):

        class Meta:

            model_class = Project

*Thats all! This code generate Table with name and description columns which has AJAX inline edit.*

.. warning::

    This project depends on Horizon library, but isn't in the requirements because we want install horizon/openstack dashboard as we want !


|Donation|_


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