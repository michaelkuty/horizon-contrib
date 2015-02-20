# -*- coding: UTF-8 -*-
from django.conf import settings
from django.utils.html import format_html
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from horizon import tables
from horizon import tabs

class BaseTabTable(tabs.TableTab):
    """base tab table which provide instance as tab.object property
    """
    @property
    def object(self):
        return self.tab_group.kwargs['instance']