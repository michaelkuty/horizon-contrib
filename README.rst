
======================
horizon django contrib
======================

What does solves ?

* ModelTable, PaginatedTable
* IndexView, PaginatedIndexView
* ModelModalForm(based on SelfhandlingForm)
* ModelFormTab, TableTab, ..

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

Modal Tabs
----------

.. code-block:: python

	from horizon_contrib.tabs import ModelFormTab, TableTab

	from .tables import NoteFormSetTable, DocumentTable

	class IssueUpdateForm(SelfHandlingModelForm):

	    class Meta:
	        model = Issue

	    def __init__(self, *args, **kwargs):

	        request = kwargs.pop("request", None)
	        issue = kwargs.pop("issue", None)

	        super(IssueUpdateForm, self).__init__(*args, **kwargs)

	        # CRISPY layout
	        self.helper.layout = TabHolder(
	            Tab(
	                u"Issue",
	                Div(
	                    'project', 'priority', 'status',
	                                'tracker', 'assigned_to', 'subject',
	                    css_class="col-lg-6 field-wrapper"
	                ),
	                Div(
	                    'start_date', 'due_date', 'description',
	                    css_class="col-lg-6 field-wrapper"
	                )
	            ),
	        )
            TableTab(
                u"Notes",
                table=NoteFormSetTable(request, data=journal_set.filter(notes__regex = r'.{1}.*')), # only with notes 
            ),
            
            documents = [..]

	        self.helper.layout.extend([TableTab(
	                u"Files",
	                table=DocumentTable(request, data=documents),
	            )])

Read more
---------

* https://www.djangoproject.com/
* http://docs.openstack.org/developer/horizon/
