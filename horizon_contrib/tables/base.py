# -*- coding: UTF-8 -*-
from operator import attrgetter

import six
from django.conf import settings
from django.core.paginator import EmptyPage, Paginator
from django.forms.models import fields_for_model
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _
from horizon import tables, exceptions
from horizon.tables import Column
from horizon.tables.base import DataTableMetaclass, DataTableOptions
from horizon_contrib.api.models import DictModel
from horizon_contrib.common.content_type import get_class

from . import filters
from .actions import UpdateColumnAction


class AjaxUpdateRow(tables.Row):
    """ row with implemented get_data for generic ajax update
    """

    ajax = True

    def get_data(self, request, id):
        instance = self.table._model_class.objects.get(id=id)
        return instance


class ModelTableOptions(DataTableOptions):

    """provide new params for Table Meta class

        .. attribute:: model_class

        String or Django Model.

        .. attribute:: order_by

        Array for ordering default is ('-id')

        .. attribute:: extra_columns is default to True

        This means if we specify some columns no extra
        columns will be generated

    """

    def __init__(self, options):

        # set our row class
        self.row_class = getattr(options, "row_class", AjaxUpdateRow)
        if options:
            setattr(options, "row_class", self.row_class)

        super(ModelTableOptions, self).__init__(options)
        self.model_class = getattr(options, 'model_class', None)
        self.order_by = getattr(options, 'order_by', ("-id"))
        self.extra_columns = getattr(options, "extra_columns", False)
        self.ajax_update = getattr(options, "ajax_update", False)
        self.update_action = getattr(
            options, "update_action", UpdateColumnAction)


class ModelTableMetaclass(DataTableMetaclass):

    def __new__(mcs, name, bases, attrs):
        # Process options from Meta
        class_name = name
        attrs["_meta"] = opts = ModelTableOptions(attrs.get("Meta", None))
        # Gather columns; this prevents the column from being an attribute
        # on the DataTable class and avoids naming conflicts.
        columns = []
        for attr_name, obj in list(attrs.items()):
            if issubclass(type(obj), (opts.column_class, Column)):
                column_instance = attrs.pop(attr_name)
                column_instance.name = attr_name
                column_instance.classes.append('normal_column')
                columns.append((attr_name, column_instance))
        columns.sort(key=lambda x: x[1].creation_counter)

        # Iterate in reverse to preserve final order
        for base in bases[::-1]:
            if hasattr(base, 'base_columns'):
                columns = list(base.base_columns.items()) + columns
        attrs['base_columns'] = OrderedDict(columns)

        # If the table is in a ResourceBrowser, the column number must meet
        # these limits because of the width of the browser.
        if opts.browser_table == "navigation" and len(columns) > 3:
            raise ValueError("You can only assign three column to %s."
                             % class_name)
        if opts.browser_table == "content" and len(columns) > 2:
            raise ValueError("You can only assign two columns to %s."
                             % class_name)

        if opts.columns:
            # Remove any columns that weren't declared if we're being explicit
            # NOTE: we're iterating a COPY of the list here!
            for column_data in columns[:]:
                if column_data[0] not in opts.columns:
                    columns.pop(columns.index(column_data))
            # Re-order based on declared columns
            columns.sort(key=lambda x: attrs['_meta'].columns.index(x[0]))
        # Add in our auto-generated columns
        if opts.multi_select and opts.browser_table != "navigation":
            multi_select = opts.column_class("multi_select",
                                             verbose_name="",
                                             auto="multi_select")
            multi_select.classes.append('multi_select_column')
            columns.insert(0, ("multi_select", multi_select))
        if opts.actions_column:
            actions_column = opts.column_class("actions",
                                               verbose_name=_("Actions"),
                                               auto="actions")
            actions_column.classes.append('actions_column')
            columns.append(("actions", actions_column))
        # Store this set of columns internally so we can copy them per-instance
        attrs['_columns'] = OrderedDict(columns)

        # Gather and register actions for later access since we only want
        # to instantiate them once.
        # (list() call gives deterministic sort order, which sets don't have.)
        actions = list(set(opts.row_actions) | set(opts.table_actions))
        actions.sort(key=attrgetter('name'))
        actions_dict = OrderedDict([(action.name, action())
                                    for action in actions])
        attrs['base_actions'] = actions_dict
        if opts._filter_action:
            # Replace our filter action with the instantiated version
            opts._filter_action = actions_dict[opts._filter_action.name]

        # Create our new class!
        return type.__new__(mcs, name, bases, attrs)


class ModelTable(six.with_metaclass(ModelTableMetaclass, tables.DataTable)):

    """
    Django model class or string(content_type).

    .. attribute:: model_class String or django model class

    note: best way is ModelClass because find by content_type
    makes additional db queries

    .. attribute:: order_by is default to ("-id")

    """

    def __init__(self, request, data=None, model_class=None,
                 needs_form_wrapper=None, **kwargs):

        super(ModelTable, self).__init__(
            request=request,
            data=data,
            needs_form_wrapper=needs_form_wrapper,
            **kwargs)

        if not hasattr(self, "model_class") and model_class:
            self.model_class = model_class

        if self._model_class and self._meta.extra_columns:
            # get fields and makes columns
            fields = fields_for_model(
                self._model_class,
                fields=getattr(self._meta, "columns", []))

            actions = self.columns.pop("actions", [])
            columns = OrderedDict()

            if not len(columns) > 0 or self._meta.extra_columns:
                many = [i.name for i in
                        self._model_class._meta.many_to_many]

                for name, field in fields.items():
                    if name not in columns:
                        column_kwargs = {
                            "verbose_name": getattr(field, "label", name),
                            "form_field": field
                        }
                        if self._meta.ajax_update:
                            column_kwargs["update_action"] = \
                                self._meta.update_action
                        if name in many:
                            column_kwargs["filters"] = filters.filter_m2m,
                        column = tables.Column(name, **column_kwargs)
                        column.table = self
                        columns[name] = column

                if actions:
                    columns["actions"] = actions

                self._columns = columns
                self.columns = columns
                self._populate_data_cache()

            self._meta.verbose_name = \
                self._model_class._meta.verbose_name_plural.title()

    def is_serialized(self):
        """try first object from filtered_data
        and serialized if none in ModelClass
        """
        datum = self._filtered_data[0]
        if isinstance(self._model_class, datum.__class__):
            return True
        return False

    @property
    def filtered_data(self):

        super(ModelTable, self).filtered_data

        if hasattr(self, '_filtered_data') and self._filtered_data is not None:
            items = []
            if not self.is_serialized:
                for datum in self._filtered_data:
                    if isinstance(datum, dict):
                        # iterate over model fields and apply some filters
                        for key, val in six.iteritems(datum):
                            if isinstance(val, list):
                                datum[key] = filters.join_list(val)
                    if self._model_class:
                        # create our object
                        model = self._model_class(**datum)
                    else:
                        # create dictionary with dotted notation
                        model = DictModel(**datum)

                        items.append(model)
                self._filtered_data = items
        return self._filtered_data

    @property
    def _model_class(self):
        mcs = getattr(self._meta, "model_class", None)
        if not mcs:
            mcs = getattr(self, "model_class", None)

        if isinstance(mcs, six.string_types) and mcs:
            try:
                mcs = get_class(mcs)
            except Exception as e:
                raise e
        return mcs

    def get_table_data(self):
        """generic implementation
        returns queryset or list dataset for paginator
        """
        object_list = []
        if self._model_class is None and not callable(self.get_table_data):
            raise Exception(
                "you must specify ``model_class`` or override get_table_data")
        object_list = self._model_class.objects.all()

        # check if is queryset
        # TODO: use native python sorted function
        if hasattr(object_list, "order_by"):
            object_list.order_by(
                self._meta.order_by)
        return object_list


class PaginationMixin(object):

    """

    Turn off render pagination into template.

    .. attribute:: pagination

    Django model class.

    .. attribute:: model_class or string(content_type) see ModelTable

        Turn off render `Show all` into template.

    .. attribute:: show_all_url

    .. attribute:: position

        Position of pagionation Top, Bottom, Both

    """
    order_by = ("-id")

    page = "1"
    pagination = True
    position = "bottom"
    show_all_url = True

    PAGINATION_COUNT = "25"
    _paginator = None

    def get_paginator_data(self):
        """generic implementation which expect modeltable inheritence
        """
        return self.get_table_data()

    @property
    def get_page(self):
        """returns int page"""
        page = None
        try:
            page = int(self.page)  # fail only if set all
        except Exception:
            # swallow
            pass
        return page

    def get_page_data(self, page="1"):
        """returns data for specific page
        default returns for first page
        """

        if not self.paginator:
            raise RuntimeError('missing paginator instance ')

        if page:
            self.page = page
        try:
            if not self.page == "all":
                objects = self.paginator.page(self.page)
            elif self.show_all_url:
                objects = self.get_paginator_data()
        except EmptyPage:
            objects = self.paginator.page(self.paginator.num_pages)
        return objects

    @property
    def paginator(self):
        """returns instance of paginator
        """
        if not self._paginator:
            try:
                self._paginator = Paginator(
                    self.get_paginator_data(), self.PAGINATION_COUNT)
            except Exception as e:
                raise e
        return self._paginator

    def previous_page_number(self):
        if self.get_page is not None:
            return self.get_page - 1
        return None

    def next_page_number(self):
        if self.get_page is not None:
            return self.get_page + 1
        return None

    def has_previous(self):
        if self.get_page is not None:
            if self.get_page == 1:
                return False
            return True
        return False

    def has_next(self):
        if self.get_page is not None:
            if (self.get_page + 1) > self.paginator.num_pages:
                return False
            return True
        return False

    @property
    def has_other_pages(self):
        return True if (self.has_previous or self.has_next) else False

    def has_more_data(self):
        """in default state is disabled, but can be used, but must be
        implemented some extra methods
        """
        return False

    def __init__(self, *args, **kwargs):

        self._meta.template = \
            "horizon_contrib/tables/_paginated_data_table.html"

        super(PaginationMixin, self).__init__(*args, **kwargs)

        self.PAGINATION_COUNT = getattr(
            settings, "PAGINATION_COUNT", self.PAGINATION_COUNT)


class PaginatedTable(PaginationMixin, ModelTable):

    """Paginated datatable with simple implementation which uses django Paginator

    note(majklk): this table uses custom table template
    """
    pass


class PaginatedModelTable(PaginatedTable):

    """named paginated table
    """


class ApiPaginatationMixin(PaginationMixin):

    show_all_url = False

    def get_page_data(self, page="1"):
        """returns data for specific page
        """

        try:
            self._paginator = self.manager.list(
                self.request,
                search_opts={'page': page})
        except Exception as e:
            self._paginator = []
            if settings.DEBUG:
                raise e
            exceptions.handle(self.request,
                              _('Unable to load %s' % self._meta.verbose_name))

        return self._paginator

    @property
    def get_page(self):
        """returns int page"""
        return self.request.GET.get('page', "1")

    def previous_page_number(self):
        if self.has_previous:
            return int(self.get_page) - 1
        return None

    def next_page_number(self):
        if self.has_next:
            return int(self.get_page) + 1
        return None

    def has_previous(self):
        return self._paginator.previous

    def has_next(self):
        return self._paginator.next


class PaginatedApiTable(ApiPaginatationMixin, ModelTable):
    '''simple api pagination table

    set manager attribute like manager = api.hosts
    '''
    pass


class ReactTable(ModelTable):

    """generic paginated model table
    """

    def __init__(self, *args, **kwargs):

        super(ReactTable, self).__init__(*args, **kwargs)

        self._meta.template = \
            "horizon_contrib/tables/_react_data_table.html"
