
from django.conf import settings
from horizon import tables
from django.utils.html import format_html

GRAPHITE_PREFIX = getattr(settings, 'GRAPHITE_PREFIX', 'stats')


class GraphColumn(tables.base.Column):

    """Simple Graph column

    wrapps data with id {{column_name}}_{{self.table.get_object_id}}
    if is not object_id provided

    :attribute:graph_id - asdadasd-asdasd-asdad-asd

    :attribute:graph_metric - libvirt.disk_ops.*.write

    """

    template = '<div id="graph_{name}_{uuid}" data-name="{name}" data-metric="{metric}"></div>'

    def __init__(self, *args, **kw):
        graph_id = kw.pop('graph_id', None)
        graph_metric = kw.pop('graph_metric', None)
        full_path = kw.pop('full_path', False)
        super(GraphColumn, self).__init__(*args, **kw)
        self.graph_id = graph_id
        self.graph_metric = graph_metric
        self.full_path = full_path

    def get_metric(self, datum):

        uuid = self.get_uuid(datum)
        if GRAPHITE_PREFIX and not self.full_path:
            return '{}.{}.{}'.format(
                GRAPHITE_PREFIX, uuid, self.graph_metric or 'specify_metric')
        elif GRAPHITE_PREFIX and self.full_path:
            return '{}.{}'.format(
                GRAPHITE_PREFIX, self.graph_metric or 'specify_metric')
        return '{}.{}'.format(uuid, self.graph_metric or 'specify_metric')

    def get_uuid(self, datum):
        return getattr(self, self.graph_id, None) or self.table.get_object_id(datum)

    def get_raw_data(self, datum):

        return format_html(
            self.template.format(**{
                'name': self.name,
                'uuid': self.get_uuid(datum),
                'metric': self.get_metric(datum)}))
