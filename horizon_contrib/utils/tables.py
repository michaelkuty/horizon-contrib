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

"""logentries"""
class BaseTabTable(tabs.TableTab):
    """spolecny predek pro taby, zjednodusuje pristup k instanci
    """
    @property
    def object(self):
        return self.tab_group.kwargs['instance']

    def get_logentries(self, instance):
        return list(LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(instance).pk,object_id=instance.pk).order_by("action_time").all())
