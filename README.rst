
|License badge| |Doc badge|

======================
horizon django contrib
======================

Library which simplify creating beautiful and powerfull web applications with Django and Horizon.

What does solves ?
------------------

* ModelTable, PaginatedTable, PaginatedModelTable (based on DataTable)
* IndexView, PaginatedView (based on DataTableView)
* ModelModalForm(based on SelfhandlingForm)
* ModelFormTab, TableTab, ..
* Actions - Filter
* filters

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


Read more
---------

* horizon-contrib.readthedocs.org
* https://www.djangoproject.com/
* https://github.com/openstack/horizon
* http://docs.openstack.org/developer/horizon/

.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat
.. |Doc badge| image:: https://readthedocs.org/projects/horizon-contrib/badge/?version=latest
