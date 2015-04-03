
===================
ReactJS Integration
===================

Why
---

For some customers we need render hundreds rows in one table with many columns and all with inline AJAX updates for each column.
With AngularJS is too slow any sotrable actions, filters and initial render is unusable.

With ReactJS we can render thousands of rows without any lags.

.. note::

    For now it's an implementation with many dysfunctions versus standard AngularJS. But ready for experimenting.

Beginnings
----------

For this purpose is there initial implementation of ReactJS SortTable which is available for some scenarios.

In previous chapter we introduced how we work with tables and their views.

GenericView has one additionaly argument which specify used table. If we want render React table for our panel we can simply set ``react=True`` on ``Panel`` class and voila our index is rendered as ReactJS table as we used to.

As you can see in the url if we append ``/react`` to our url contrib render ReactJS table.
For example our index ``contrib/models/<my_class>/index/`` and append ``/react`` finally we have ``contrib/models/<my_class>/index/react/``

Usage
-----

.. code-block:: bash

    pip install xstatic-react

Add to ``settings.py``

.. code-block:: python

    import xstatic.pkg.react

    STATICFILES_DIRS = [
        ('lib', xstatic.main.XStatic(xstatic.pkg.react).base_dir),

    ]

* ``/contrib/models/project/react`` ..

In the Panel

.. code-block:: python

    from horizon_contrib.panel import ModelPanel
    from horizon_redmine.dashboard import RedmineDashboard

    class ProjectPanel(ModelPanel):
        name = "Projects"
        slug = 'projects'
        model_class = 'project'

        react = True

    RedmineDashboard.register(ProjectPanel)

As table

.. code-block:: python

    from horizon_contrib.tables import ReactTable


    class MyReactTable(ReactTable):

        ...

.. note::

    For now we use the in-browser JSX transformer.

ReactJS DataTable
-----------------

.. code-block:: html

    var Table = Reactable.Table;
    var Tr = Reactable.Tr;
    var Td = Reactable.Td;

    var HorizonReactDataTable = React.createClass({
      getInitialState: function(){
        return {data: []};
      },  
      render: function(){
        return (
        <Table
          id="{{ table.slugify_name }}" 
          className="{% block table_css_classes %}table table-bordered table-striped datatable {{ table.css_classes }}{% endblock %}"
          sortable={true}
          data={this.state.data}
          >
        {% for row in rows %}

          <Tr{{ row.attr_string|safe }}>
              {% spaceless %}
                  {% for cell in row %}
                     <Td{{ cell.attr_string|safe }}>{%if cell.wrap_list %}<ul>{% endif %}{{ cell.value }}{%if cell.wrap_list %}</ul>{% endif %}</Td>
                  {% endfor %}
              {% endspaceless %}
              <Td>{{ row.render_row_actions }}</Td>
          </Tr>

        {% endfor %}

        </Table>
        )
      },
      componentDidMount: function() {
        $.ajax({
          url: this.props.url,
          dataType: 'json',
          success: function(data) {
            this.setState({data: data});
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
     }
    });
    /* here we expect url/json as data url */
    React.renderComponent(<HorizonReactDataTable url="json"/>,
    document.getElementById('{{ table.slugify_name }}'));


.. note::

    Implementation uses ``https://github.com/glittershark/reactable``