
from horizon_contrib.tables.actions import (CreateAction, DeleteAction,
                                            FilterAction, UpdateAction,
                                            UpdateColumnAction)
from horizon_contrib.tables.base import (ModelTable, PaginatedModelTable,
                                         PaginatedTable)
from horizon_contrib.tables.views import IndexView, PaginatedView

CD_ACTIONS = (DeleteAction,CreateAction)
ROW_ACTIONS = (UpdateAction,DeleteAction)
TABLE_ACTIONS = CD_ACTIONS + (FilterAction,)
