
from horizon_contrib import tables


class GenericTable(tables.PaginatedTable):
    """
    Generic table

    .. attribute:: cls_name String or django model class

    note: best way is ModelClass because find by content_type
    makes additional db queries

    .. attribute:: order_by is default to ("-id")

    note: table requires python objects or we must override
    ``get_object_id`` and ``get_object_display``

    """

    def get_object_display(self, datum):
        return str(datum)

    def get_object_id(self, datum):
        """try id as default pk
        if not defined ``primary_key=True``
        must be defined on one of model fields
        """
        if datum:
            if not isinstance(datum, dict):
                if hasattr(datum._meta, 'pk'):
                    id = getattr(datum, 'id', None)
                elif hasattr(datum._meta, 'pk'):
                    id = getattr(datum, str(datum._meta.pk.name))
            else:
                id = datum.get('id')
        return id

    def __init__(self, *args, **kwargs):

        if 'cls_name' in kwargs:
            self.model_class = kwargs.pop('cls_name', None)

        super(GenericTable, self).__init__(*args, **kwargs)

        if 'table' in kwargs:
            self.table_type = kwargs.pop('table', None)
            self._meta.template = \
                "horizon_contrib/tables/_react_data_table.html"

    class Meta:
        table_actions = tables.TABLE_ACTIONS
        row_actions = tables.ROW_ACTIONS
        extra_columns = True
        ajax_update = True
