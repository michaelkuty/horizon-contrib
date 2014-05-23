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

class BaseIndexView(tables.DataTableView):
    """view s obecne implementovanou metodou get_data
    hodi se predevsim jako index view lze jej ale pouzit i na jine pohledy
    staci overridnout metody na dane table view viz. BaseTable
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