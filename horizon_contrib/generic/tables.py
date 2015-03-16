
from horizon_contrib import tables


class GenericTable(tables.ModelTable):

    def get_object_display(self, datum):
        return datum.__unicode__()

    def get_object_id(self, datum):
        id = getattr(datum, 'id', None)
        if not id and isinstance(datum, dict):
            id = datum.get('id', self.get_object_display())
        return id

    class Meta:

        table_actions = tables.TABLE_ACTIONS
        row_actions = tables.ROW_ACTIONS
        extra_columns = True
