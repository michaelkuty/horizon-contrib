
## Todo

* [x] refactoring and cleanup obsolete and unless stuff
* [x] for vanilla horizon usage must be extended DataTableOptions
* [x] support for generic table from model class - construct table from model.fields
* [ ] make generic views for index(PaginatedTable), create(ModalForm), update(ModalForm), delete(BatchAction)
* [ ] implement custom fields and lookups on FilterAction
* [ ] BaseClient and refactor API module
* [ ] TESTS !
* [ ] Pep8 cleanup

## Generic views and Actions

*  (horizon_contrib/<model_name>/index)
*  (horizon_contrib/<model_name>/create)
*  (horizon_contrib/<model_name>/<model_id>/update)
*  (horizon_contrib/<model_name>/<model_id>/delete)