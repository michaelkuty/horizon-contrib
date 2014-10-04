# -*- coding: utf-8 -*-

import datetime
from horizon import messages
from django import forms as django_forms
from django.conf import settings
from horizon import forms
from django.forms.extras.widgets import SelectDateWidget
from horizon_contrib.forms.models import create_or_update_and_get

try:
    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Div
    CRISPY = True
except Exception, e:
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
    """
    required_css_class = 'required'

    def api_error(self, message):
        """Adds an error to the form's error dictionary after validation
        based on problems reported via the API. This is useful when you
        wish for API errors to appear as errors on the form rather than
        using the messages framework.
        """
        self._errors[NON_FIELD_ERRORS] = self.error_class([message])

    def set_warning(self, message):
        """Sets a warning on the form.

        Unlike NON_FIELD_ERRORS, this doesn't fail form validation.
        """
        self.warnings = self.error_class([message])

    def __init__(self, request, *args, **kwargs):
        self.request = request
        if not hasattr(self, "handle"):
            raise NotImplementedError("%s does not define a handle method."
                                      % self.__class__.__name__)
        super(SelfHandlingMixin, self).__init__(*args, **kwargs)

        # crispy layout
        if CRISPY:
            self.helper = FormHelper(self)
            self.helper.field_class = ""
            self.helper.form_tag = False
            self.helper.label_class = "control-label"

            # classes added only if not hidden
            for item in self.helper.layout.fields:
                if item in ["object_id", "id"]:
                    continue
                self.helper[item].wrap(Div, css_class="col-lg-6 field-wrapper")


class SelfHandlingForm(SelfHandlingMixin, django_forms.Form):

    """modal form with default crispy layout
    """

    pass


class SelfHandlingModelForm(SelfHandlingMixin, django_forms.ModelForm):

    """form with implemented handle method
    """

    def handle(self, request, data):
        model = None
        try:
            model = self.Meta.model
        except Exception, e:
            raise e
        if not model:
            raise Exception("Missing model")
        try:
            saved_model = create_or_update_and_get(model, data)
            try:
                messages.success(
                    request, u"Model %s byl uložen." % saved_model)
            except Exception, e:
                raise e
                # swallowed Exception
                # model has not __unicode__ method
        except Exception, e:
            if getattr(settings, "DEBUG", False):
                messages.error(request, e.message)
                messages.error(request, data)
            return False
        return True