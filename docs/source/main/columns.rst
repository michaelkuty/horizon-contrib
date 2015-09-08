
=======
Columns
=======

For some common scenarios are there some generic columns which may help you with daily tasks.

Linked List Column
------------------

This columns is same as standard column when you use ``link`` Attribute, but this columns takes array of items and makes link for every item. For example if you have list of devices and you want make detail link for every item in this table and separate it with comma then::

    class MyTable(Table):

        devices = LinkedListColumn(
            'devices', verbose_name=_("Devices"),
            url="horizon:dashboard:devices:update")

        devices = LinkedListColumn(
            ...,
            url="horizon:dashboard:devices:update", datum_pk='key', label='item.name')

Graph Column
------------

This column redner graph from Graphite. Basically it's just simple column with integrated cubism.js.

Using this column requires two steps. First you need define your  ``GraphColumn`` with metric and then you need inicialize JavaScript on client side.

GraphColumn

.. code-block:: python

	from horizon_contrib.tables.columns import GraphColumn

	class AdminHypervisorsTable(tables.DataTable):
	    host = tables.Column("host",
	                         link=("horizon:admin:hypervisors:detail"),
	                         verbose_name=_("Host"))

	    cpu = GraphColumn('hostname',
                          verbose_name=_("CPU Utilisation"),
                          graph_metric='cpu.*.*',
                          graph_id="host",
                          )

Template 

.. code-block:: html

	{% block js %}

	{{ block.super }}

	<script type="text/javascript" src="{{ STATIC_URL }}horizon_contrib/js/cubism.js"></script>
	<script type="text/javascript" src="{{ STATIC_URL }}horizon_contrib/js/graph_utils.js"></script>

	<script type="text/javascript">

	$(function() {

	var graphite_endpoint = "{{ graphite }}";

	// from which column you want draw axis
	draw_axis('usage', 2, 6);

	draw_graphs("table tbody tr", graphite_endpoint);

	});

	</script>
	{% endblock %}