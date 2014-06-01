# -*- coding: UTF-8 -*-
from django.conf import settings
from django.utils.html import format_html
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from horizon import tables
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from horizon import exceptions
from horizon import tabs

class LogEntryTable(tables.DataTable):
    """django LogEntryTable
    """

    @staticmethod
    def get_logentries(instance):
        return list(LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(instance).pk,object_id=instance.pk).order_by("action_time").all())

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
    #todo predelat field z cisel na string 1 => create
    action_flag = tables.Column('action_flag', verbose_name=_("Typ akce"),
                                                filters=(get_flag_name,))

    class Meta:
        name = _("Historie")