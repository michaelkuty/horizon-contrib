
======================
horizon django contrib
======================

What does solves ?

* ModelTable, PaginatedTable, PaginatedModelTable (based on DataTable)
* IndexView, PaginatedView (based on DataTableView)
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


        class Meta:

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

note: for easy table inheritence we supports model_class directly on the table class

.. code-block:: python

    ...
    
    class MyModelTable(ModelTable):

        model_class = MyModelClass
    
    ...


Specifing columns and ordering
------------------------------

.. code-block:: python

    class MyModelTable(ModelTable):


        class Meta:
            columns = ("project", "issue", ..)
            order_by = ("id") # queryset.order_by(self._meta.order_by)

note: order by is used for generic queryset for more customization please override get_table_data


Custom queryset
---------------

.. code-block:: python

    class MyModelTable(ModelTable):

        def get_table_data(self):
            return self._model_class.objects.all().order_by("status__id")


PaginatedTable
--------------

`tables.py`

.. code-block:: python

    from horizon_contrib.tables.base import PaginatedTable

    class MyModelTable(PaginatedTable):


        class Meta:
        
            model_class = MyModelClass

and then `views.py`

.. code-block:: python

    from horizon_contrib.tables.views import PaginatedView

    from .tables import MyModelTable

    class IndexView(IndexView):
        table_class = MyModelTable


PaginatedModelTable
-------------------

this table combine ModelTable and Pagination

.. code-block:: python

    from horizon_contrib.tables import PaginatedModelTable

    class MyModelTable(PaginatedModelTable):

        model_class = "mymodelclass"


and then `views.py`

.. code-block:: python

    from horizon_contrib.tables.views import PaginatedView

    from .tables import PaginatedModelTable

    class IndexView(IndexView):
        table_class = PaginatedModelTable


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
