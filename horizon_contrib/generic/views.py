
import json

from django.http import HttpResponse
from horizon_contrib import tables
from horizon_contrib.common import get_class

from .tables import GenericTable


class GenericIndexView(tables.IndexView):

    """contruct table from model class

    .. attribute:: cls_name

    String which represent model_class.__name__

    .. attribute:: table

    String which represent table type accept react and angular is default

    """

    table_class = GenericTable
    template_name = 'horizon_contrib/tables/index.html'
    react_template_name = 'horizon_contrib/tables/react_index.html'

    def get_template_names(self):
        table_type = self.kwargs.get('table', 'angular')
        if table_type == 'react':
            return [self.react_template_name]
        return [self.template_name]

    @property
    def model_class(self):
        return get_class(self.kwargs["cls_name"])

    def get_context_data(self, **kwargs):
        context = super(GenericIndexView, self).get_context_data(**kwargs)
        context['title'] = getattr(
            self.model_class._meta, 'verbose_name_plural',
            self.model_class._meta.verbose_name).title()
        return context

    def get_data(self):
        # ReactJS loads data from client-side
        table_type = self.kwargs.get('table', 'angular')
        if table_type == 'react':
            return []
        return super(GenericIndexView, self).get_data()


class ReactGenericView(GenericIndexView):

    """using extended template with ReactJS dependencies
    """

    template_name = 'horizon_contrib/tables/react_index.html'

    def get_data(self):
        return []


class DataView(GenericIndexView):

    """returns all data for specific model_cls in json format

    .. attribute:: cls_name

    """

    def get(self, request, cls_name, table=None):
        data = self.get_table().get_table_data()
        return HttpResponse(json.dumps(data), content_type='application/json')
