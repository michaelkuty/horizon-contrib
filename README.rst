
======================
horizon django contrib
======================

What does solves ?

* ModelTable, PaginatedDataTable
* IndexView, PaginatedIndexView
* ModelModalForm(based on SelfhandlingForm)


Show me
=======


ModelTable
----------

`tables.py`

.. code-block:: python

	from horizon_contrib.tables.base import ModelTable

	from .models import MyModelClass

	class MyModelTable(ModelTable):

	    model_class = MyModelClass
	    
	    # or as string, but this makes some additional db queries
	    model_class = "mymodelclass"


and then `views.py`

.. code-block:: python

	from horizon_contrib.tables.views import IndexView

	from .tables import MyModelTable

	class IndexView(BaseIndexView):
	    table_class = MyModelTable
	    template_name = 'myapp/mymodel/index.html' # or leave blank


PaginatedTable
--------------

`tables.py`

.. code-block:: python

	from horizon_contrib.tables.base import PaginatedTable

	class MyModelTable(PaginatedTable):

	    model_class = "mymodelclass"


and then `views.py`

.. code-block:: python

	from horizon_contrib.tables.views import PaginatedView

	from .tables import MyModelTable

	class IndexView(BaseIndexView):
	    table_class = MyModelTable


SelfHandlingModelForm
---------------------

`forms.py`

.. code-block:: python

	from horizon_contrib.forms import SelfHandlingModelForm

	class IssueCreateForm(SelfHandlingModelForm):

	    class Meta:
	        model = Issue
	        fields = ['project', 'priority', 'description', 'due_date']
	        widgets = {
	            'description': Textarea,
	            'due_date': DateTimeWidget(attrs={'id': "due_date"}, options=settings.DATE_PAST_OPTIONS)
	        }
	    
	    # handle it or leave blank or call super where is implemented basic logic for saving models
	    # but in many cases is not sufficient and we must override this
	    def handle(self, request, data, model_class):

	        model_instance = model_class.objects.get(id=data.pop("object_id"))

`views.py`

.. code-block:: python

	from horizon_contrib import ModalFormView

	class CreateView(ModalFormView):

	    form_class = IssueCreateForm
	    success_url = "horizon:redmine:..."

	    template_name = 'redmine/issue/create.html'

Read more
---------

* https://www.djangoproject.com/
* http://docs.openstack.org/developer/horizon/
