# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from horizon import tables


class ContextMixin(object):

    def get_name(self):
        return getattr(self, 'name', self.__class__.__name__)

    def get_title(self):
        return self.get_name() + _(' of ') + \
            self.get_table()._model_class._meta.verbose_name


class IndexView(ContextMixin, tables.DataTableView):

    """view with implemented get_data where recall table.get_table_data
    """

    template_name = 'horizon_contrib/tables/index.html'  # or leave blank

    def get_data(self):
        objects = []
        table = self.get_table()
        if table:
            try:
                objects = table.get_table_data()
            except NotImplementedError as e:
                raise e
            return objects
        else:
            return None


class PaginatedView(IndexView):

    """basic pagiated view
    """

    def get_data(self):
        objects = []
        table = self.get_table()
        page = self.request.GET.get('page', None)
        if table:
            if page:
                try:
                    objects = table.get_page_data(page=page)
                except NotImplementedError as e:
                    raise e
            else:
                objects = table.get_page_data()  # defaultne 1
            return objects
        return objects
