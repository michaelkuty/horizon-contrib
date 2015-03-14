
from horizon_contrib.tables.base import (ModelTable, PaginatedModelTable,
                                         PaginatedTable)
from horizon_contrib.tables.views import IndexView, PaginatedView
from horizon_contrib.tables.actions import FilterAction, DeleteAction

CRUD_ACTIONS = (DeleteAction,)
