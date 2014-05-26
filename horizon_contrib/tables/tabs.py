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
    """spolecny predek pro taby, zjednodusuje pristup k instanci
    """
    @property
    def object(self):
        return self.tab_group.kwargs['instance']

    def get_logentries(self, instance):
        return list(LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(instance).pk,object_id=instance.pk).order_by("action_time").all())
