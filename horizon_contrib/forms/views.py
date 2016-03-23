

import json
import os

from django import http
from django.forms import models as model_forms
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.views import generic
from horizon import exceptions
from importlib import import_module
from horizon_contrib.common import content_type as ct
from django.forms.models import model_to_dict
from horizon_contrib.forms.forms import SelfHandlingModelForm

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


class ContextMixin(object):

    """provide common getters for form views

    TODO(majklk): name in past and present + model unicode !
    """

    def get_name(self):
        return getattr(self, 'name', self.__class__.__name__)

    def get_label(self):
        model_name = u"%s" % self.model._meta.verbose_name
        return self.get_name() + ' ' + u"%s" % model_name

    def get_form_id(self):
        return b"%s" % self.get_label()

    def get_header(self):
        return b"%s" % self.get_label()

    def get_help_text(self):
        return getattr(self, 'help_text', _('Empty space is so boring please\
                                            provide `help_text on this view`'))


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
        return getattr(obj, 'name', obj.__class__.__name__)

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""

        kwargs = self.get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return form_class(**kwargs)

    def form_valid(self, form):
        try:
            handled = form.handle(self.request, form.cleaned_data)
        except Exception as e:
            raise e
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
                    response = http.HttpResponseRedirect(
                        self.request.META.get('HTTP_REFERER', success_url))
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

    def get_context_data(self, **kwargs):
        context = super(ModalFormView, self).get_context_data(**kwargs)

        # add extra context for template
        context['url'] = self.request.build_absolute_uri()
        context['modal_size'] = self._get_moda_size()

        return context

    def _get_moda_size(self):
        '''try get form_size attribute form form or widget'''
        if hasattr(self, 'model'):
            form_class = self.get_form_class()
            return getattr(form_class,
                           'form_size',
                           getattr(self.model, 'form_size', 'md'))
        return 'md'


class ModelModalView(ModalFormView):

    pass


class ModelFormMixin(object):

    def _get_class_from_string(self, path):
        mod = '.'.join(path.split('.')[0:-1])
        cls_name = path.split('.')[-1]
        return getattr(import_module(mod), cls_name)

    @cached_property
    def object(self):

        try:
            obj = self.model.objects.get(id=self.kwargs["id"])
        except Exception as e:
            raise e
        return obj

    @cached_property
    def model(self):
        # TODO if not content_type FW find in our registry
        return ct.get_class(self.kwargs["cls_name"])

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'request': self.request
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form_class(self):
        """
        Returns the form class to use in this view.
        """

        if 'form_cls' in self.kwargs:
            try:
                form_class = self._get_class_from_string(
                    self.kwargs['form_cls'])
            except ImportError:
                # use standard form instead of raising exception
                pass
            else:
                return model_forms.modelform_factory(self.model, exclude=[],
                                                     form=form_class)

        if self.form_class:
            return self.form_class
        else:
            if self.model is not None:
                # If a model has been explicitly provided, use it
                model = self.model
            elif hasattr(self, 'object') and self.object is not None:
                # If this view is operating on a single object, use
                # the class of that object
                model = self.object.__class__
        return model_forms.modelform_factory(model, exclude=[],
                                             form=SelfHandlingModelForm)


class CreateView(ModelFormMixin, ModalFormView, ContextMixin):

    name = _('Create')

    template_name = 'horizon_contrib/forms/create.html'

    success_url = "/"  # for now

    def get_form(self, form_class):
        """Returns an instance of the form to be used in this view."""
        return self.get_form_class()(**self.get_form_kwargs())

    def get_success_url(self):
        if self.request.META.get("HTTP_REFERER") != \
                self.request.build_absolute_uri():
            return self.request.META.get('HTTP_REFERER')
        return super(CreateView, self).get_success_url()

    def form_valid(self, form):

        handled = None
        success_url = self.get_success_url()

        # handle is priotiry
        if hasattr(form, 'handle'):

            handled = super(CreateView, self).form_valid(form)

        elif hasattr(form, 'save'):

            try:
                instance = form.save()
            except Exception as e:
                raise e
            else:
                if hasattr(form, 'handle_related_models'):
                    # handle related models
                    form.handle_related_models(self.request, instance)

                try:
                    success_url = instance.get_absolute_url()
                except Exception as e:
                    try:
                        success_url = instance.page.get_absolute_url()
                    except:
                        pass

        response = http.HttpResponseRedirect(success_url)
        response['X-Horizon-Location'] = success_url

        return handled or response

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)

        # add extra context for template
        context['url'] = self.request.build_absolute_uri()
        context['form_id'] = self.get_form_id()
        context['modal_header'] = self.get_header()
        context['title'] = self.get_header()
        context['view_name'] = self.name
        context['heading'] = self.get_header()
        context['help_text'] = self.get_help_text()

        return context

    def get_initial(self):
        return {}


class UpdateView(CreateView):
    form_class = None
    template_name = 'horizon_contrib/forms/create.html'

    name = _('Update')

    def get_initial(self):
        if isinstance(self.object, dict):
            return self.object
        return model_to_dict(self.object)
