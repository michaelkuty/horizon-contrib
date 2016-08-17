

from django import forms as django_forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from horizon import forms, messages
from django.utils.encoding import smart_text

try:
    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Div, Layout, HTML
    from crispy_forms.bootstrap import Tab, TabHolder
    CRISPY = True
except Exception as e:
    CRISPY = False


class DateForm(forms.Form):

    """A simple form for selecting a range of time."""
    start = forms.DateField(input_formats=("%Y-%m-%d", "%d.%m.%Y"))
    end = forms.DateField(input_formats=("%Y-%m-%d", "%d.%m.%Y"))

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['start'].widget.attrs['data-date-format'] = "dd-mm-yyyy"
        self.fields['end'].widget.attrs['data-date-format'] = "dd-mm-yyyy"


class SelfHandlingMixin(object):

    """A base :class:`Form <django:django.forms.Form>` class which includes
    processing logic in its subclasses.

        tabs = {
            'tab1': {
                'name': 'Verbose Name'
                'fields': ('field_name1',)
            }
        }

        help_text = "Select user and role."

    """
    required_css_class = 'required'

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        if not hasattr(self, "handle"):
            raise NotImplementedError("%s does not define a handle method."
                                      % self.__class__.__name__)
        super(SelfHandlingMixin, self).__init__(*args, **kwargs)

        # crispy layout
        if CRISPY and not hasattr(self, 'helper'):
            self.helper = FormHelper(self)
            self.helper.field_class = ""
            self.helper.form_tag = False
            self.helper.label_class = "control-label"

            if hasattr(self, 'help_text'):
                # for helptext make two columns
                self.helper[0:len(self.helper.layout.fields)].wrap_together(
                    Div, css_class="col-lg-6 field-wrapper")
                self.helper.layout.append(
                    HTML(smart_text("<div class='col-lg-6 help-text'>%s</div>" % self.help_text)))
            else:
                # classes added only if not hidden
                for item in self.helper.layout.fields:
                    if item in ["object_id", "id"]:
                        continue
                    try:
                        self.helper[item].wrap(
                            Div, css_class="col-lg-6 field-wrapper")
                    except Exception:
                        pass

    def init_layout(self):
        '''Call init for generic layout'''
        self.helper.layout = Layout(TabHolder())
        self.init_custom_tabs()

    def get_tabs(self):
        '''Merge form tabs with models tabs'''
        tabs = getattr(self._meta.model, 'tabs', {})
        tabs.update(getattr(self, 'tabs', {}))
        return tabs

    def init_custom_tabs(self):
        '''init custom tabs
        tabs = {
            'tab1': {
                'name': 'Verbose Name'
                'fields': ('field_name1',)
            }
        }
        '''
        for tab_name, tab in self.get_tabs().items():
            self.insert_tab(tab.get('name', tab_name), tab['fields'])

    def get_main_fields(self, fields):
        '''filter field which are included in custom tab'''
        _fields = []
        for field in fields:
            if field not in self._custom_fields():
                _fields.append(field)
        return _fields

    def _custom_fields(self):
        '''returns acumulated fields from ``tabs``'''
        fields = []
        if not hasattr(self, '__custom_fields'):
            for tab_name, tab in self.get_tabs().items():
                fields += list(tab['fields'])
            self.__custom_fields = fields
        return self.__custom_fields

    def insert_tab(self, name, fields, position=1):
        '''Push tab to specific position
        in the default state is after main widget tab
        '''
        self.helper.layout[0].insert(
            position,
            Tab(name,
                *fields
                )
        )


class SelfHandlingForm(SelfHandlingMixin, django_forms.Form):

    """modal form with default crispy layout
    """

    pass


class SelfHandlingModelForm(SelfHandlingMixin, django_forms.ModelForm):

    """form with implemented handle method
    """

    def handle(self, request, data):

        instance = self.save()

        messages.success(
            request,
            _(smart_text("Model %s was successfuly saved." % instance)))

        if hasattr(self, 'handle_related_models'):
            # handle related models
            self.handle_related_models(self.request, instance)

        return instance
