
==============
Generic module
==============

This module provide same functionality as Django Admin, but in AngularJS cloak with custom actions, modal forms client side categorizing, filtering and many more.

With Horizon
------------

Dashboard structure::

    |-- my_dashboard
        |-- __init__.py
        |-- projects
            |-- __init__.py
            |-- models.py
            |-- forms.py
            |-- managers.py
            |-- urls.py
            |-- views.py
        |-- issues
            |-- __init__.py
            |-- panel.py
        |-- dashboard.py

Simply register your ModelClass and connect it to ModelPanel which provides namespace and menu item.

.. code-block:: python

    from horizon import forms
    from horizon_contrib.api import models
    from horizon_contrib.common import register_model
    
    from .managers import ProjectManager

    class Project(models.APIModel):

        ...

        objects = ProjectManager()  # connect our manager

        class Meta:
            abstract = True
            verbose_name = "Project"
            verbose_name_plural = "Projects"

    register_model(Project)  # supply django Content Types

.. info:

    We have plan for autodiscover and registering models on demand.

.. code-block:: python

    from horizon_contrib.panel import ModelPanel
    from horizon_redmine.dashboard import RedmineDashboard

    class ProjectPanel(ModelPanel):
        name = "Projects"
        slug = 'projects'
        model_class = 'project'

    RedmineDashboard.register(ProjectPanel)

With Django
-----------

With Django is all stuff generic we can only used or override some parts of how we want.

Dashboard structure::

    my_app
        |-- __init__.py
        |-- models.py
        |-- my_dashboard
            |-- __init__.py
            |-- projects
                |-- __init__.py
                |-- panel.py
                |-- forms.py
                |-- tables.py
                |-- urls.py
                |-- views.py
            |-- issues
                |-- __init__.py
                |-- panel.py
            |-- dashboard.py

With reverse
------------

.. code-block:: python

    from django.core.urlresolvers import reverse
    
    print reverse('horizon:contrib:generic:index', args=['project'])

    # render as ReactJS table
    print reverse('horizon:contrib:generic:index', args=['project', 'react'])


.. warning::

	For these purpose must be ``django.contrib.contenttypes`` in ``INSTALLED_APPS``.