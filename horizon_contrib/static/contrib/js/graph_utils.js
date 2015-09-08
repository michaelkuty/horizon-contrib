

function draw_graphs(selector, graphite_endpoint) {

  $("body").find(selector).each(function (i, el){ 

      var id = el.attributes["data-object-id"];
      // jquery doesn't support dot in selector
      id = id.value.replace(/\./g,'\\.');

      $(el).find("td div").each(function(i, el) {

        if (typeof id !== "undefined") {

            type = $(el).attr('data-name');
            if (type !== "undefined") {
              draw_graph(id, type, graphite_endpoint);
            }
            //draw_graph(id, "memory_mb_used");
            //draw_graph(id, "local_gb");
            //draw_graph(id, "local_gb_used");
                
        } else {
            console.debug("No instances");
        }
        
      });
  });
}

function draw_graph(id, type, graphite_endpoint) {
    /* main function for rendering graphs */

    horizon = init_cubism(graphite_endpoint);

    var graph_id = "#graph_" + type + "_" + id;
    metric = $(graph_id).attr('data-metric');
  
    d3.select(graph_id)                 
      .selectAll(".horizon")           
      .data([metric])
      .enter()                         
      .insert("div", ".bottom")        // Insert the graph in a div. Turn the div into  
      .attr("class", "horizon")        // a horizon graph and format to 2 decimals places.
      .call(horizon);
    
}

function get_context() {
    var context = cubism.context()
                        .step(1 * 60 * 1000) // 1 minute
                        .size(360) // Number of data points
                        .stop();   // Fetching from a static data source; don't update values
    return context;    
}


function get_graphite(graphite_endpoint) {
    return get_context().graphite(graphite_endpoint);
}


function init_cubism(graphite_endpoint){
    /*
      inicialization of horizon-cubism
    */

    var context = get_context();
    var graphite = context.graphite = get_graphite(graphite_endpoint)
    var horizon = context.horizon();

    horizon = horizon.metric(graphite.metric);//.height(100).shift( - 0 * 24 * 60 * 60 * 1000 );

    // hide metric name
    horizon.title(function(d){return ""});

    return horizon;    
}


function draw_axis(id, from, to){
    /* simple helper which draw graph axis in header
    you must prive main select which is usually id of table and next
    from-to is integers which specifies columns where wi will rener axis
    */
    // draw axis :D
    for (i = from; i < to; i++) { 
      d3.select("#" + id + " > thead > tr:nth-child(2) > th:nth-child("+ i +")")                 // Select the div on which we want to act           
        .selectAll(".axis")              // This is a standard D3 mechanism to bind data
        .data(["top"])                   // to a graph. In this case we're binding the axes
        .enter()                         // "top" and "bottom". Create two divs and give them
        .append("div")                   // the classes top axis and bottom axis respectively. 
        .attr("class", function(d) {      
          return d + " axis";           
        })                             
        .each(function(d) {              // For each of these axes, draw the axes with 4 
          d3.select(this)              // intervals and place them in their proper places.
            .call(get_context().axis()       // 4 ticks gives us an hourly axis.
            .ticks(4).orient(d));      
        });
    }

}

