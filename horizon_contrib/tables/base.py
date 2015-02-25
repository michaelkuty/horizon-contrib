# -*- coding: UTF-8 -*-
import copy
from operator import attrgetter
from django.conf import settings
from django.utils.html import format_html
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from horizon import tables
from horizon.tables import Column
from django.utils.datastructures import SortedDict
from horizon import tabs
from horizon import forms
import six
from django.forms.models import fields_for_model
from django.db import models
from horizon_contrib.common.content_type import get_class


class ModelTableMixin(object):

    @property
    def _model_class(self):
        mcs = getattr(
            self._meta, "model_class", getattr(self, "model_class", None))
        if isinstance(mcs, basestring):
            try:
                self.model_class = get_class(mcs)
            except Exception, e:
                raise e
        mcls = getattr(self, "model_class", mcs)
        if not mcls:
            raise Exception(
                "Missing model_class or override one of get_table_data, get_paginator_data")
        return mcls

    def get_table_data(self):
        """generic implementation
        returns queryset or list dataset for paginator
        """
        object_list = []
        if self._model_class is None and not callable(self.get_table_data):
            raise Exception(
                "you must specify ``model_class`` or override get_table_data")
        object_list = self._model_class.objects.all().order_by(getattr(self, "order_by", "-id"))
        return object_list


def filter_m2m(datum):
    """helper for aggregation of m2m relation
    """
    items = []
    for d in datum.all():
        items.append(d.__unicode__())
    return ", ".join(items)


class ModelTable(tables.DataTable, ModelTableMixin):

    """
    Django model class or string(content_type).

    .. attribute:: model_class String or django model class

    note: best way is ModelClass because find by content_type makes additional db queries

    .. attribute:: order_by is default to ("-id")

    """

    order_by = "-id"

    def __init__(self, request, data=None, needs_form_wrapper=None, **kwargs):

        super(ModelTable, self).__init__(
            request=request, data=data, needs_form_wrapper=needs_form_wrapper, **kwargs)

        # get fields and makes columns
        fields = fields_for_model(self._model_class, fields=getattr(self._meta, "columns", []))

        columns = {}

        many = [i.name for i in self._model_class._meta.many_to_many]

        for name, field in fields.iteritems():
            column_kwargs = {
                "verbose_name": getattr(field, "label", name),
                "form_field": field
            }
            if name in many:
                column_kwargs["filters"] = filter_m2m,
            column = tables.Column(name, **column_kwargs)
            column.table = self
            columns[name] = column

        actions = self._columns.pop("actions")
        columns["actions"] = actions
        self._columns.update(columns)
        self.columns.update(columns)
        self._populate_data_cache()

        super(ModelTable, self).__init__(
            request=request, data=data, needs_form_wrapper=needs_form_wrapper, **kwargs)

        has_get_table_data = hasattr(
            self, 'get_table_data') and callable(self.get_table_data)

        if not has_get_table_data and not hasattr(self, "model_class"):
            cls_name = self.__class__.__name__
            raise NotImplementedError('You must define either a model_class or "get_table_data" '
                                      'method on %s.' % cls_name)


class PaginationMixin(ModelTableMixin):

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
        except Exception, e:
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
            except Exception, e:
                raise e
        return self._paginator

    def previous_page_number(self):
        if not self.get_page is None:
            return self.get_page - 1
        return None

    def next_page_number(self):
        if not self.get_page is None:
            return self.get_page + 1
        return None

    def has_previous(self):
        if not self.get_page is None:
            if self.get_page == 1:
                return False
            return True
        return False

    def has_next(self):
        if not self.get_page is None:
            if (self.get_page + 1) > self.paginator.num_pages:
                return False
            return True
        return False

    def has_more_data(self):
        """defaultne vypnuty staci zapnout a doimplementovat potrebne veci viz doc dorizonu"""
        return False

    def __init__(self, *args, **kwargs):
        super(PaginationMixin, self).__init__(*args, **kwargs)


class PaginatedTable(tables.DataTable, PaginationMixin):

    """Paginated datatable with simple implementation which uses django Paginator

    note(majklk): this table uses custom table template
    """

    def __init__(self, *args, **kwargs):

        self._meta.template = "horizon_contrib/tables/_paginated_data_table.html"

        super(PaginatedTable, self).__init__(*args, **kwargs)

        has_get_table_data = hasattr(
            self, 'get_paginator_data') and callable(self.get_paginator_data)

        if not has_get_table_data and not hasattr(self, "model_class"):
            cls_name = self.__class__.__name__
            raise NotImplementedError('You must define either a model_class or "get_paginator_data" '
                                      'method on %s.' % cls_name)

        self.PAGINATION_COUNT = getattr(
            settings, "PAGINATION_COUNT", self.PAGINATION_COUNT)


class PaginatedModelTable(ModelTable, PaginationMixin):

    """generic paginated model table
    """

    def __init__(self, *args, **kwargs):

        self._meta.template = "horizon_contrib/tables/_paginated_data_table.html"

        super(PaginatedModelTable, self).__init__(*args, **kwargs)

        has_get_table_data = hasattr(
            self, 'get_paginator_data') and callable(self.get_paginator_data)

        if not has_get_table_data and not hasattr(self, "model_class"):
            cls_name = self.__class__.__name__
            raise NotImplementedError('You must define either a model_class or "get_paginator_data" '
                                      'method on %s.' % cls_name)

        self.PAGINATION_COUNT = getattr(
            settings, "PAGINATION_COUNT", self.PAGINATION_COUNT)
