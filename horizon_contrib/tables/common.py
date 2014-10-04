# -*- coding: UTF-8 -*-
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.utils.html import format_html
from horizon import tables

class LogEntryTable(tables.DataTable):
    """horizon table for django log entries
    """

    def get_flag_name(flag_id):
        if flag_id == 1:
            return u"Přidání"
        elif flag_id == 2:
            return u"Změna"
        elif flag_id == 3:
            return u"Smazání"
        return "Undefined flag !!"

    def get_link(model):
        return model.pk

    content_type = tables.Column('content_type', verbose_name=_(u"Model"))
    datetime = tables.Column('action_time', verbose_name=_(u"Datum a čas"))
    user = tables.Column('user', verbose_name=_(u"Uživatel"))
    osoba = tables.Column('user', verbose_name=_(u"Osoba"), filters=(lambda user: user.first_name + " " + user.last_name,))
    change_message = tables.Column('change_message', verbose_name=_(u"Zpráva o změně"))
    action_flag = tables.Column('action_flag', verbose_name=_("Typ akce"), 
                                                filters=(get_flag_name,))
