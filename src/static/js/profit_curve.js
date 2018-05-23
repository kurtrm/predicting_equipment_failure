"use strict";
(function(window, document) {
// I leaned heavily on D3 documentation and lots of examples to generate this code.

  var svg = d3.select("#profit_curve"),
      margin = {top: 20, right: 20, bottom: 30, left: 20},
      width = +svg.attr("width") - 400 - margin.left - margin.right,
      height = +svg.attr("height") - margin.top - margin.bottom;


  var x = d3.scaleLinear()
      .range([0, width]);

  var y = d3.scaleLinear()
      .range([0, height]);

  var line = d3.line()
      .x(d => x(d.threshold))
      .y(d => y(d.loss));

  var g = svg.append("g")
      .attr("transform", "translate(" + (margin.left + 50) + "," + margin.top + ")");

if (localStorage.getItem("data") === null) {
  d3.json("/retrieve_profit_curve", function(thisData) {
    draw(thisData);
  });
} else {
  var storage = JSON.parse(localStorage["data"]);
  draw(storage);
};


function draw(data) {
  $("svg").empty()
  var x = d3.scaleLinear()
      .range([0, width]);

  var y = d3.scaleLinear()
      .range([0, height]);

  var line = d3.line()
      .x(d => x(d.threshold))
      .y(d => y(d.loss));

  var y_max = d3.max(data, d => d.loss);
  var x_val = data.filter(d => d.loss === y_max)[0].threshold;
  var horiz = [{"x1": 0.0, "y1": y_max}, {"x1": x_val, "y1": y_max}]
  var vert = [{"x2": x_val, "y2": d3.min(data, d => d.loss)}, {"x2": x_val, "y2": y_max}]

  var horiz_line = d3.line()
      .x(d => x(d.x1))
      .y(d => y(d.y1));

  var vert_line = d3.line()
      .x(d => x(d.x2))
      .y(d => y(d.y2));

  var g = svg.append("g")
      .attr("transform", "translate(" + (margin.left + 50) + "," + margin.top + ")");
  
  x.domain([0, d3.max(data, d => d.threshold)]);
  y.domain([d3.max(data, d => d.loss), d3.min(data, d => d.loss)]);

  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x))
    .append("text")
     .attr("class", "axis-title")
     .attr("y", 18)
     .attr("dy", "1em")
     .attr("x", (height/2) - 40)
     .attr("dx", "1em")
     .style("text-anchor", "start")
     .attr("fill", "#5D6971")
     .text("Threshold");

  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y))
   .append("text")
     .attr("class", "axis-title")
     .attr("transform", "rotate(-90)")
     .attr("y", -42)
     .attr("dy", ".1em")
     .attr("x", -height/2 + 30)
     .attr("dx", ".1em")
     .style("text-anchor", "end")
     .attr("fill", "#5D6971")
     .text("Cost ($)");

  var line_stuff = g.selectAll(".line")
      .data([data]);

  line_stuff.enter().append("path").classed("line", true)
             .merge(line_stuff)
             .attr("d", line)
             .attr("fill", "none")
             .attr("stroke", "black")
             .attr("stroke-dasharray", function(d) {
               return this.getTotalLength()
             })
             .attr("stroke-dashoffset", function(d) {
               return this.getTotalLength()
             });

  g.append("path")
      .datum(horiz)
      .attr("class", "horiz_line")
      .style("stroke-dasharray", ("3, 3"))
      .attr("d", horiz_line);

  g.append("path")
      .datum(vert)
      .attr("class", "vert_line")
      .style("stroke-dasharray", ("3, 3"))
      .attr("d", vert_line);

  g.append("text")
      .attr("class", "max_thresh")
      .attr("x", x(x_val))
      .attr("dx", "2em")
      .attr("y", y(y_max))
      .style("text-anchor", "end")
      .text(Math.round(x_val * 100) / 100);


  g.selectAll(".line")
    .transition()
    .duration(1000)
    .ease(d3.easeLinear)
    .attr("stroke-dashoffset", 0);

}

  $(document).ready(function() {
    $(".assessment-card").hide()
    $("button#calculate").click(function() {
      $(".assessment-card").show()
      $(".assess-box").children("button").remove();
      $("p#assessment").text("Loading...")
      $("html, body").animate({
        scrollTop: "+=100"},
        100);
      let metrics = get_metrics();
      send_metrics(metrics);
    })
  })

  let send_metrics = function(metrics) {
    $.ajax({
      url: '/generate',
      contentType: "application/json; charset=utf-8",
      type: 'POST',
      data: JSON.stringify(metrics),
      success: function(data) {
        draw(data);
        statement(data);
      }
    });
  }

  let get_metrics = function() {
    let revenue = $("input#revenue").val()
    let maintenance = $("input#maintenance").val()
    let repair = $("input#repair").val()
    return {"user_input": [revenue, maintenance, repair]}
  };

  function statement(data) {
    var threshold = parseFloat($("text.max_thresh").text()) * 100;
    var threshold_statement = threshold + "% is the optimal threshold for the given revenue, maintenance, and repair costs. Would you like to save this threshold?"
    $("p#assessment").text(threshold_statement)
    var cancel = $('<button type="button" class="btn btn-danger mr-3" id="cancel">Cancel</button>').click(function() {
      $(".assessment-card").hide()
      $(".assess-box").empty().append('<p id="assessment"></p>')
    });
    var save = $('<button type="button" class="btn btn-success ml-3" id="save">Save</button>').click(function() {
      localStorage.setItem('data', JSON.stringify(data));
      localStorage.setItem('threshold', JSON.stringify(threshold));
      localStorage.setItem('metrics', JSON.stringify(get_metrics()));
      localStorage.setItem('cost', JSON.stringify(d3.max(data, d => d.loss)));
      localStorage.setItem('rightNow', JSON.stringify(new Date()));
      $.ajax({
        url: '/calculate_metrics',
        contentType: "application/json; charset=utf-8",
        type: "POST",
        data: JSON.stringify({"threshold": threshold,
                              "data": data,
                              "metrics": get_metrics()}),
        success: function(data) {
          localStorage.setItem("precision", JSON.stringify(data['precision']));
          localStorage.setItem("recall", JSON.stringify(data['recall']));
          localStorage.setItem("f1", JSON.stringify(data['f1']));
          location.reload();
        }
      })
      // This code saved for posterity. This makes an ajax request to save data to a database.
      // Until security is implemented, data is persisted in localstorage just to demonstrate functionality.

      // $.ajax({
      //   url: '/save_profit_curve',
      //   contentType: "application/json; charset=utf-8",
      //   type: 'POST',
      //   data: JSON.stringify({"threshold": threshold,
      //                         "data": data,
      //                         "metrics": get_metrics()}),
      //   success: function() {
      //   location.reload();
      //   }
      // })

    });
    $(".assess-box").append(cancel).append(save)
  }
})(window, document);