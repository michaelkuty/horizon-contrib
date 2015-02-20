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


from horizon_contrib.common.content_type import get_class

class ModelTableMixin(object):


    @property
    def _model_class(self):
        if isinstance(self.model_class, basestring):
            try:
                self.model_class = get_class(self.model_class)
            except Exception, e:
                raise e
        return self.model_class


class ModelTable(tables.DataTable, ModelTableMixin):

    """
    Django model class or string(content_type).
    
    .. attribute:: model_class String or django model class

    note: best way is ModelClass because find by content_type makes additional db queries
    
    .. attribute:: order_by is default to ("-id")
    
    """

    order_by = ("-id")

    def __init__(self, *args, **kwargs):
        super(ModelTable, self).__init__(*args, **kwargs)

        has_get_table_data = hasattr(self, 'get_table_data') and callable(self.get_table_data)

        if not has_get_table_data and not hasattr(self, "model_class"):
            cls_name = self.__class__.__name__
            raise NotImplementedError('You must define either a model_class or "get_table_data" '
                                      'method on %s.' % cls_name)

    def get_table_data(self):
        """generic implementation
        returns queryset or list dataset for paginator
        """
        object_list = []
        if self._model_class is None and not callable(self.get_table_data):
            raise Exception("you must specify ``model_class`` or override get_table_data")
        object_list = self._model_class.objects.all().order_by(self.order_by)
        return object_list


class PaginationMixin(object):

    """ Turn off render pagination into template.

    .. attribute:: pagination

    Django model class.

    .. attribute:: model_class or string(content_type) see ModelTable

        Turn off render `Show all` into template.

    .. attribute:: show_all_url

    .. attribute:: position

        Position of pagionation Top, Bottom, Both

    """

    page = "1"
    pagination = True
    position = "bottom"
    show_all_url = True
   
    PAGINATION_COUNT = "25"
    _paginator = None
    
    def get_paginator_data(self):
        return self.get_table_data()

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
            raise RuntimeError('missing paginator instance ')

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
               self._paginator =  Paginator(self.get_paginator_data(), self.PAGINATION_COUNT) 
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

    def __init__(self, *args, **kwargs):
        super(PaginationMixin, self).__init__(*args, **kwargs)
    

class PaginatedTable(ModelTable, PaginationMixin):

    def __init__(self, *args, **kwargs):

        self._meta.template = "horizon_contrib/tables/_paginated_data_table.html"

        super(PaginatedTable, self).__init__(*args, **kwargs)

        has_get_table_data = hasattr(self, 'get_paginator_data') and callable(self.get_paginator_data)

        if not has_get_table_data and not hasattr(self, "model_class"):
            cls_name = self.__class__.__name__
            raise NotImplementedError('You must define either a model_class or "get_paginator_data" '
                                      'method on %s.' % cls_name)

        self.PAGINATION_COUNT =  getattr(settings, "PAGINATION_COUNT", self.PAGINATION_COUNT) 