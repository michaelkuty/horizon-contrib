# -*- coding: utf-8 -*- 
from horizon import forms as horizon_forms
from django import forms as django_forms

class SelfHandlingMixin(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        if not hasattr(self, "handle"):
            raise NotImplementedError("%s does not define a handle method."
                                      % self.__class__.__name__)
        super(SelfHandlingMixin, self).__init__(*args, **kwargs)


class SelfHandlingModelForm(SelfHandlingMixin, django_forms.ModelForm):
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