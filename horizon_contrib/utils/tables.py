# -*- coding: UTF-8 -*-
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import urlresolvers
from django.template.defaultfilters import timesince
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from horizon import tables
from horizon import tabs

class PaginatedTable(tables.DataTable):
    """base table s paginatorem a jeho pomocnyma metodama
    u table staci specifikovat model_name:String (lze pouzivat i bez nej, ale musi byt nejakym zpusobem overridnouta)
    paginator lze pretizit bud overridnutim metody get_paginator_data
    nebo rovnou overridnutim property paginator na dane tabulce
    defaultne je vypnuty defaultni horajzni paginator, lze zapnout overridnutim has_more_data 
    """

    """ Turn off render pagination into template.

    .. attribute:: pagination

        Turn off render `Show all` into template.

    .. attribute:: show_all_url

    """

    page = "1"
    pagination = True
    show_all_url = True
    
    PAGINATION_COUNT = "25"
    _paginator = None

    def __init__(self, *args, **kwargs):
        super(PaginatedTable, self).__init__(*args, **kwargs)

        has_get_data = hasattr(self, 'get_paginator_data') and callable(self.get_paginator_data)

        if not has_get_data:
            cls_name = self.__class__.__name__
            raise NotImplementedError('You must define either a "get_paginator_data" '
                                      'method on %s.' % cls_name)

        try:
            self.PAGINATION_COUNT = settings.PAGINATION_COUNT
        except Exception, e:
            pass

    def get_paginator_data(self):
        """must be overwritten
        returns queryset or list dataset for paginator
        """
        pass
    
    def get_page(self):
        """returns int page"""
        return int(self.page)

    def get_page_data(self, page=None):
        """returns data for specific page
        default returns for first page
        """
        
        if not self.paginator:
            raise RuntimeError('missing paginator instance %s.' % cls_name)

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
               self._paginator = Paginator(self.get_paginator_data(), self.PAGINATION_COUNT) 
            except Exception, e:
                raise e
        return self._paginator

    def previous_page_number(self):
        return int(self.page) - 1

    def next_page_number(self):
        return int(self.page) + 1

    def has_previous(self):
        if int(self.page) == 1:
            return False
        return True

    def has_next(self):
        if (int(self.page) + 1) > self.paginator.num_pages:
            return False
        return True

    def has_more_data(self):
        """defaultne vypnuty staci zapnout a doimplementovat potrebne veci viz doc dorizonu"""
        return False
    """
    def get_pagination_string(self):
        return "page=%s"% self.page
    """

class AgregateMixin(tables.base.Column):
    """return html array of links for all models"""
    
    detail_url = "horizon:common:osoba:detail"
    
    field = None #must be M2M field
    
    #object mus have __unidoce__ and pk !!

    def get_raw_data(self, datum):
        output = []
        if self.field:
            objects = getattr(datum, self.field)
            for obj in objects.all():
                url = reverse(self.detail_url, args=[obj.pk,])
                link = u"<a href='%s'>%s</a>" % (url, obj)
                output.append(link)
        return format_html(', '.join(output))

class BaseAgregateMixin(object):
    """returns html table for django model with nested fields
    class Pohledavka(models.Model):

        test_field = models.ManyToManyField("Nested")

    class Nested(models.Model):

        test_field1 = Charfield etc..
        test_field2 = ..

    field = test_field
    nested_fields = ("test_field1", "test_field2")
    """
    
    field = None #must be M2M field
    _thead = None #readonly
    nested_fields = None

    def thead(self, obj):
        if len(self.nested_fields) > 0:
            tds = []
            for label in self.nested_fields:
                if label:
                    field_name = "field name"
                    try:
                        field_name = obj._meta.get_field_by_name(label)[0].name
                        field_name = obj._meta.get_field_by_name(label)[0].verbose_name
                    except Exception, e:
                        raise e
                    field_label = field_name.capitalize()
                    td = u"<td>{0}</td>".format(field_label)
                    tds.append(td)
            tr = u"<tr>{0}</tr>".format("".join(tds))
            thead = u"<thead>{0}</thead>".format("".join(tr))
            return format_html(thead)
        return None

    def get_raw_data(self, datum):
        if self.field:
            objects = getattr(datum, self.field)
            trs = []
            for obj in objects.all():
                if self._thead is None and obj:
                    self._thead = self.thead(obj)
                tds = []
                for field in self.nested_fields:
                    if field:
                        value = getattr(obj, field)
                        td = u"<td>{0}</td>".format(value)
                        tds.append(td)
                tr = u"<tr>{0}</tr>".format("".join(tds))
                trs.append(tr)
            table = u"<table>{0}{1}</table>".format(self._thead, "".join(trs))
            return format_html(table)
        return None

"""logentries"""
class BaseTabTable(tabs.TableTab):
    """spolecny predek pro taby, zjednodusuje pristup k instanci
    """
    @property
    def object(self):
        return self.tab_group.kwargs['instance']

    def get_logentries(self, instance):
        return list(LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(instance).pk,object_id=instance.pk).order_by("action_time").all())
