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

from horizon_contrib.tables.views import PaginatedView

class BaseIndexView(PaginatedView):
    """obsolete, will be removed, use table.views instead
    """
    pass