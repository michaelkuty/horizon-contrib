import json
import os
from django import http
from django.views import generic

from horizon import exceptions


ADD_TO_FIELD_HEADER = "HTTP_X_HORIZON_ADD_TO_FIELD"


class ModalFormMixin(object):
    def get_template_names(self):
        if self.request.is_ajax():
            if not hasattr(self, "ajax_template_name"):
                # Transform standard template name to ajax name (leading "_")
                bits = list(os.path.split(self.template_name))
                bits[1] = "".join(("_", bits[1]))
                self.ajax_template_name = os.path.join(*bits)
            template = self.ajax_template_name
        else:
            template = self.template_name
        return template

    def get_context_data(self, **kwargs):
        context = super(ModalFormMixin, self).get_context_data(**kwargs)
        if self.request.is_ajax():
            context['hide'] = True
        if ADD_TO_FIELD_HEADER in self.request.META:
            context['add_to_field'] = self.request.META[ADD_TO_FIELD_HEADER]
        return context

class ModalFormView(ModalFormMixin, generic.FormView):
    """The main view class from which all views which handle forms in Horizon
    should inherit. It takes care of all details with processing
    :class:`~horizon.forms.base.SelfHandlingForm` classes, and modal concerns
    when the associated template inherits from
    `horizon/common/_modal_form.html`.

    Subclasses must define a ``form_class`` and ``template_name`` attribute
    at minimum.

    See Django's documentation on the `FormView <https://docs.djangoproject.com
    /en/dev/ref/class-based-views/generic-editing/#formview>`_ class for
    more details.
    """

    def get_object_id(self, obj):
        """For dynamic insertion of resources created in modals, this method
        returns the id of the created object. Defaults to returning the ``id``
        attribute.
        """
        return obj.id

    def get_object_display(self, obj):
        """For dynamic insertion of resources created in modals, this method
        returns the display name of the created object. Defaults to returning
        the ``name`` attribute.
        """
        return obj.name

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        try:
            handled = form.handle(self.request, form.cleaned_data)
        except Exception:
            handled = None
            exceptions.handle(self.request)

        if handled:
            if ADD_TO_FIELD_HEADER in self.request.META:
                field_id = self.request.META[ADD_TO_FIELD_HEADER]
                data = [self.get_object_id(handled),
                        self.get_object_display(handled)]
                response = http.HttpResponse(json.dumps(data))
                response["X-Horizon-Add-To-Field"] = field_id
            elif isinstance(handled, http.HttpResponse):
                return handled
            else:
                success_url = self.get_success_url()
                if self.request.META.get("HTTP_REFERER") != self.request.build_absolute_uri():
                    response = http.HttpResponseRedirect(self.request.META.get('HTTP_REFERER', success_url))
                else:
                    response = http.HttpResponseRedirect(success_url)
                # TODO(gabriel): This is not a long-term solution to how
                # AJAX should be handled, but it's an expedient solution
                # until the blueprint for AJAX handling is architected
                # and implemented.
                response['X-Horizon-Location'] = success_url
            return response
        else:
            # If handled didn't return, we can assume something went
            # wrong, and we should send back the form as-is.
            return self.form_invalid(form)

class ModelModalView(ModalFormMixin, generic.FormView):
    """The main view class from which all views which handle forms in Horizon
    should inherit. It takes care of all details with processing
    :class:`~horizon.forms.base.SelfHandlingForm` classes, and modal concerns
    when the associated template inherits from
    `horizon/common/_modal_form.html`.

    Subclasses must define a ``form_class`` and ``template_name`` attribute
    at minimum.

    See Django's documentation on the `FormView <https://docs.djangoproject.com
    /en/dev/ref/class-based-views/generic-editing/#formview>`_ class for
    more details.

    form_class = SelfHandlingModelForm
    template_name = ``string``

    def get_context_data(self, **kwargs):
        pass

    def get_initial(self):
        pass
    often you can use django model_to_dict(model)
    """
    def get_object_id(self, obj):
        """For dynamic insertion of resources created in modals, this method
        returns the id of the created object. Defaults to returning the ``id``
        attribute.
        """
        return obj.id

    def get_object_display(self, obj):
        """For dynamic insertion of resources created in modals, this method
        returns the display name of the created object. Defaults to returning
        the ``name`` attribute.
        """
        return obj.name

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        try:
            handled = form.handle(self.request, form.cleaned_data)
        except Exception:
            handled = None
            exceptions.handle(self.request)

        if handled:
            if ADD_TO_FIELD_HEADER in self.request.META:
                field_id = self.request.META[ADD_TO_FIELD_HEADER]
                data = [self.get_object_id(handled),
                        self.get_object_display(handled)]
                response = http.HttpResponse(json.dumps(data))
                response["X-Horizon-Add-To-Field"] = field_id
            elif isinstance(handled, http.HttpResponse):
                return handled
            else:
                #TODO reverse url
                success_url = self.get_success_url()
                response = http.HttpResponseRedirect(success_url)
                # TODO(gabriel): This is not a long-term solution to how
                # AJAX should be handled, but it's an expedient solution
                # until the blueprint for AJAX handling is architected
                # and implemented.
                response['X-Horizon-Location'] = success_url
            return response
        else:
            # If handled didn't return, we can assume something went
            # wrong, and we should send back the form as-is.
            return self.form_invalid(form)