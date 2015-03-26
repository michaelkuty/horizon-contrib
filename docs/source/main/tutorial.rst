
==============
Short tutorial
==============

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

*Your* models.py

.. code-block:: python

    from django import models

    class Project(models.Model):

        name = models.CharField..
        description = models.CharField..
        ...

        class Meta:
            verbose_name = 'Project'

Include our urls.

.. code-block:: python


    from django.conf.urls import patterns, include, url

    urlpatterns = patterns('',
        ...
        url(r'^contrib/', include('horizon_contrib.urls', namespace='horizon'), ),
        ...
    )

Visit these urls

.. code-block:: python

    /contrib/models/<model_name>/index/
    /contrib/models/<model_name>/create/
    /contrib/models/<model_name>/<model_id>/update/

.. note::

    For these purpose must be ``django.contrib.contenttypes`` in ``INSTALLED_APPS``.

REST API Dashboards
-------------------

Dashboard structure::

    my_dashboard
        |-- __init__.py
        |-- projects
            |-- __init__.py
            |-- managers.py
            |-- models.py
            |-- panel.py
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

Manager usual usage.

``utils/redmine_client.py``

.. code-block:: python

    from django.conf import settings
    from horizon_contrib.api import Manager

    class RedmineManager(Manager):

        # here will change client behaviour

        # def request(...)

        def set_api(self):
            self.api = '%s://%s:%s' % (
                settings.REDMINE_PROTOCOL,
                settings.REDMINE_HOST,
                settings.REDMINE_PORT)

``managers.py``

.. code-block:: python

    from django.conf import settings
    from ..utils.redmine_client import RedmineManager

    class ProjectManager(RedmineManager):

        def all(self, *args, **kwargs):
            return self.request('/projects')