
from django.core import urlresolvers
from django.utils.html import format_html
from horizon import tables


class LinkedListColumn(tables.Column):

    """LinkedList column

    column for generic lists with link actions
    similar with single link action

    .. code-block:: python

        extensions = LinkedListColumn(
            'extensions', verbose_name=_("Extensions"),
            url="horizon:location:hosts:update")

        extensions = LinkedListColumn(
            ...,
            url="horizon:location:hosts:update", datum_pk='key', label='item.name')

    """

    url = "horizon:location:real_devices:update"

    link_html = '<a class="ajax-modal" href="{url}">{label}</a>'

    def __init__(self, *args, **kwargs):
        self.url = kwargs.pop('url')
        self.label = kwargs.pop('label', None)
        self.datum_pk = kwargs.pop('datum_pk', None)
        super(LinkedListColumn, self).__init__(*args, **kwargs)

    def get_datum(self, datum):
        '''similar to get_raw_data
        '''
        return datum[self.name]

    def get_raw_data(self, datum):
        self.datum = datum
        # collect all links
        if isinstance(self.get_datum(datum), list):
            links = []
            for item in self.get_datum(datum):
                links.append(self.render_link(item))
            return format_html(', '.join(links))
        # return single link
        return self.render_link(datum)

    def render_link(self, datum):
        '''render link to html
        '''
        return format_html(
            self.link_html.format(**self.get_link_context(datum)))

    def get_arguments(self, datum):
        '''returns arguments to url reverse
        '''
        return [self.get_object_id(datum)]

    def get_link_url(self, datum):
        '''returns reversed single url
        '''
        return urlresolvers.reverse_lazy(
            self.url, args=self.get_arguments(datum))

    def get_link_context(self, datum):
        '''returns context to format link'''
        return {
            'url': self.get_link_url(datum),
            'label': self.get_object_display(datum)
        }

    def get_object_id(self, datum):
        '''returns object id
        support nested dictionary paths like host.hostname
        '''
        if self.datum_pk:
            if self.datum_pk == "table_datum":
                return self.table.get_object_id(self.datum)
            return self._get_nested(datum, self.datum_pk)
        return self.table.get_object_id(datum)

    def get_object_display(self, datum):
        '''returns labels from item
        uses table.get_object_display if is not provided
        support nested dictionary paths like host.hostname
        '''
        if self.label:
            return self._get_nested(datum, self.label)
        return self.table.get_object_display(datum)

    def _get_nested(self, datum, key):
        '''small helper which supports nested dictionaries'''
        parts = key.split('.')
        if len(parts) == 2:
            return datum[parts[0]][parts[1]]
        return datum[key] if isinstance(datum, dict) else datum
