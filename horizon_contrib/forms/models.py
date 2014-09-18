# -*- coding: utf-8 -*- 
from horizon import forms as horizon_forms
from horizon import messages
from django import forms as django_forms
from django.conf import settings
from django.db import models

try:
    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Div
    CRISPY = True
except Exception, e:
    CRISPY = False

"""
these method is used in ``SelfHandlingModalForm`` for easily save model
because django <1.7 not supported update_or_create
https://docs.djangoproject.com/en/1.7/ref/models/querysets/#django.db.models.query.QuerySet.update_or_create
"""

def create_or_update_and_get(model_class, data):
    # note we assume data is already deserialized to a dict
    if model_class._meta.pk.name in data:
        get_or_create_kwargs = {
            model_class._meta.pk.name: data.pop(model_class._meta.pk.name)
        }
        try:
            # get
            instance = model_class.objects.get(**get_or_create_kwargs)
        except model_class.DoesNotExist:
            # create
            instance = model_class(**get_or_create_kwargs)
    else:
        # create
        instance = model_class()
 
    # update (or finish creating)
    for key,value in data.items():
        field = model_class._meta.get_field(key)
        if not field:
            continue
        if isinstance(field, models.ManyToManyField):
            # can't add m2m until parent is saved
            continue
        elif isinstance(field, models.ForeignKey) and hasattr(value, 'items'):
            rel_instance = create_or_update_and_get(field.rel.to, value)
            setattr(instance, key, rel_instance)
        else:
            setattr(instance, key, value)
    instance.save()
    # now add the m2m relations
    for field in model_class._meta.many_to_many:
        if field.name in data and hasattr(data[field.name], 'append'):
            for obj in data[field.name]:
                rel_instance = create_or_update_and_get(field.rel.to, obj)
                getattr(instance, field.name).add(rel_instance)
    return instance

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

    with automatic save model
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
                messages.success(request, u"Model %s byl uložen." % saved_model)
            except Exception, e:
                raise e
                #swallowed Exception
                #model has not __unicode__ method
        except Exception, e:
            if getattr(settings, "DEBUG", False):
                messages.error(request, e.message)
                messages.error(request, data)
            return False
        return True

    def __init__(self, *args, **kwargs):
        super(SelfHandlingModelForm, self).__init__(*args, **kwargs)
        
        # crispy layout
        if CRISPY:
            self.helper = FormHelper(self)
            self.helper.field_class = ""
            self.helper.form_tag = False
            self.helper.label_class = "control-label"
            self.helper.all().wrap(Div, css_class="col-lg-6 field-wrapper")