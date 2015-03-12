# -*- coding: UTF-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import http
from django.conf import settings
from django import shortcuts
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict
from django.views.generic import edit
from horizon import tables


class IndexView(tables.DataTableView):
    """view with implemented get_data where recall table.get_table_data
    """

    template_name = 'horizon_contrib/tables/index.html' # or leave blank

    def get_data(self):
        objects = []
        table = self.get_table()
        if table:
            try:
                objects = table.get_table_data()
            except NotImplementedError, e:
                raise e
            return objects
        else:
            return None


class PaginatedView(tables.DataTableView):
    """basic pagiated view
    """

    def get_data(self):
        objects = []
        table = self.get_table()
        page = self.request.GET.get('page', None)
        if table:
            if page:
                try:
                    objects = table.get_page_data(page=page)
                except NotImplementedError, e:
                    raise e
            else:
                objects = table.get_page_data() #defaultne 1
            return objects
        else:
            """chybi table mel by zarvat i horizon"""
            return None