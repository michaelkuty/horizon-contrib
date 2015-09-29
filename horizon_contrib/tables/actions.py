# -*- coding: UTF-8 -*-

from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from django.utils import six


class BaseFilterAction(tables.FilterAction):

    """filter action for search in all available columns

    .. attribute:: custom_field

        Custom field for search. Default is all fields.

    TODO: implement fields attr

    fields = ['name', 'subject']

    lookups = ['project__name']

    """
    needs_preloading = True

    def filter_number_data(self, table, data, filter_string):
        return self.filter(table, data, filter_string)

    def filter_timestamp_data(self, table, data, filter_string):
        return self.filter(table, data, filter_string)

    def filter(self, table, data, filter_string):
        q = filter_string.lower()

        def comp(obj):
            if isinstance(obj, dict):
                for key, value in six.iteritems(obj):
                    if q in str(obj.get(key, "")).lower():
                        return True
            if isinstance(obj, object):
                try:
                    for prop in obj._meta.fields:
                        name = prop.name
                        if q in str(obj.__dict__[name]):
                            return True
                except Exception:
                    # swallowed exception
                    pass
            return False

        return list(filter(comp, data))


class FilterAction(BaseFilterAction):
    pass


class UpdateColumnAction(object):
    """A table action for cell updates by inline editing."""

    name = "update"
    action_present = _("Update")
    action_past = _("Updated")

    data_type_singular = 'Instance'

    def action(self, request, datum, obj_id, cell_name, new_cell_value):
        self.update_cell(request, datum, obj_id, cell_name, new_cell_value)

    def update_cell(self, request, datum, obj_id, cell_name, new_cell_value):
        """Method for saving data of the cell.

        This method must implements saving logic of the inline edited table
        cell.
        """

        setattr(datum, cell_name, new_cell_value)
        datum.save()

    def allowed(self, request, datum, cell):
        """Determine whether updating is allowed for the current request.

        This method is meant to be overridden with more specific checks.
        Data of the row and of the cell are passed to the method.
        """
        return True


class CreateAction(tables.LinkAction):

    name = "create_instance"
    verbose_name = "Create"
    url = "horizon:contrib:forms:create"
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self, instance=None):
        model_cls = self.table._model_class
        model_name = ".".join([model_cls._meta.app_label, model_cls.__name__])
        return urlresolvers.reverse_lazy(self.url, args=[model_name])


class UpdateAction(tables.LinkAction):

    name = "update_instance"
    verbose_name = "Update"
    url = "horizon:contrib:forms:update"
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self, instance):
        model_cls = self.table._model_class
        model_name = ".".join([model_cls._meta.app_label, model_cls.__name__])
        obj_id = getattr(instance, model_cls._meta.pk.name, 'id')
        return urlresolvers.reverse_lazy(
            self.url, args=[model_name, obj_id])


class DeleteAction(tables.DeleteAction):
    action_present = ("Delete",)
    action_past = ("Deleted",)
    name = "delete"

    # FIX ME
    data_type_singular = 'Instance'

    def delete(self, request, obj_id=None):
        if obj_id:
            instance = self.table._model_class.objects.get(
                **{self.table._model_class._meta.pk.name: obj_id})
            instance.delete()

    def allowed(self, request, instance):
        return True

    def __init__(self, **kwargs):
        super(DeleteAction, self).__init__(**kwargs)
        self.success_url = kwargs.get('success_url', None)
