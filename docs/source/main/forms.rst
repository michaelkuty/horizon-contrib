
=====
Forms
=====

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

    from horizon_contrib.forms import ModalFormView

    class CreateView(ModalFormView):

        form_class = IssueCreateForm
        success_url = "horizon:redmine:..."

        template_name = 'redmine/issue/create.html'

or simple use our ``CreateView`` which is based on SelfHandlingForm but use Django ModelForm

here we can specified fields array which be used for modelform factory or our ``form_class``.

CreateView
----------

.. code-block:: python

    from horizon_contrib.forms import CreateView

    class CreateView(CreateView):

        name = _('Create Whatever') # your "action" name 

        form_class = None # your form 
        template_name = 'horizon_contrib/forms/create.html' # your template

        success_url = ...


UpdateView
----------

Nothing special here. This view is same as ``CreateView``, but tries getting initial data


Modal Tabs
----------

You can use standard Horizon Workflows, but for many scenarios we need custom tabs with simply describe.

.. code-block:: python

    from horizon_contrib.tabs import ModelFormTab, TableTab
    from horizon_contrib.forms import SHMForm # shortcat for SelfHandlingModelForm

    from .tables import NoteFormSetTable, DocumentTable

    class IssueUpdateForm(SHMForm):

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
