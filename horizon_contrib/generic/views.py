
from horizon_contrib import tables
from horizon_contrib.common import get_class

from .tables import GenericTable


class GenericIndexView(tables.PaginatedView):

    """contruct table from model class
    """

    table_class = GenericTable

    @property
    def model_class(self):
        return get_class(self.kwargs["cls_name"])

    def get_context_data(self, **kwargs):
        context = super(GenericIndexView, self).get_context_data(**kwargs)
        context['title'] = self.model_class._meta.verbose_name
        return context

    def get_data(self):
        objects = []
        try:
            objects = self.get_table().get_table_data()
        except Exception, e:
            raise e
        return objects
