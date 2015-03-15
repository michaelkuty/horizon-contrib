
from horizon_contrib import tables


class GenericTable(tables.ModelTable):

    def get_object_display(self, datum):
        return datum.__unicode__()

    def get_object_id(self, datum):
        return datum.pk

    class Meta:

        table_actions = tables.TABLE_ACTIONS
        row_actions = tables.ROW_ACTIONS
        extra_columns = True
