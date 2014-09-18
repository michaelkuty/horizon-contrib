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
from horizon import tabs

class PaginationTable(tables.DataTable):
    """base table s paginatorem a jeho pomocnyma metodama
    u table staci specifikovat model_name:String (lze pouzivat i bez nej, ale musi byt nejakym zpusobem overridnouta)
    paginator lze pretizit bud overridnutim metody get_paginator_data
    nebo rovnou overridnutim property paginator na dane tabulce
    defaultne je vypnuty defaultni horajzni paginator, lze zapnout overridnutim has_more_data 
    """

    """ Turn off render pagination into template.

    .. attribute:: pagination

    Django model class.

    .. attribute:: model_class

        Turn off render `Show all` into template.

    .. attribute:: show_all_url

    .. attribute:: position

        Position of pagionation Top, Bottom, Both

    """
    model_class = None
    page = "1"
    pagination = True
    position = "bottom"
    show_all_url = True
    
    PAGINATION_COUNT = "25"
    _paginator = None

    def __init__(self, *args, **kwargs):
        super(PaginationTable, self).__init__(*args, **kwargs)

        has_get_data = hasattr(self, 'get_paginator_data') and callable(self.get_paginator_data)

        if not has_get_data:
            cls_name = self.__class__.__name__
            raise NotImplementedError('You must define either a "get_paginator_data" '
                                      'method on %s.' % cls_name)

        self.PAGINATION_COUNT =  getattr(settings, "PAGINATION_COUNT", self.PAGINATION_COUNT) 

    def get_paginator_data(self):
        """must be overwritten
        returns queryset or list dataset for paginator
        """
        object_list = []
        if self.model_class is None and not callable(self.get_paginator_data):
            raise Exception("you must specify ``model_class`` or override get_paginator_data")
        try:
            object_list = self.model_class.objects.all().order_by("-id")
        except Exception, e:
            raise e
        return object_list

    @property
    def get_page(self):
        """returns int page"""
        page = None
        try:
            page = int(self.page) #fail only if set all
        except Exception, e:
            pass
        return page

    def get_page_data(self, page="1"):
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
    """
    def get_pagination_string(self):
        return "page=%s"% self.page
    """

