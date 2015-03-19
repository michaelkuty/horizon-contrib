
==============
Generic module
==============

This module provide same functionality as Django Admin, but in AngularJS cloak with custom actions, modal forms client side categorizing, filtering and many more.

With Horizon
------------

Simply register your ModelPanel which has defined ``model_class``.

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

With reverse
------------

.. code-block:: python

    from django.core.urlresolvers import reverse
    
    print reverse('horizon:contrib:generic:index', args=['project'])

    # render as ReactJS table
    print reverse('horizon:contrib:generic:index', args=['project', 'react'])


.. warning::

	For these purpose must be ``django.contrib.contenttypes`` in ``INSTALLED_APPS``.