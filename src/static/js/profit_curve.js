"use strict";

/*
This code is not DRY. the d3.json internals 

*/

var svg = d3.select("svg"),
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

d3.json("static/data/thresh_losses.json", function(thisData) {
  draw(thisData);
});

let get_metrics = function() {
  let revenue = $("input#revenue").val()
  let maintenance = $("input#maintenance").val()
  let repair = $("input#repair").val()
  return {"user_input": [revenue, maintenance, repair]}
};

let draw = function(data) {
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

  d3.selectAll("g").transition().duration(3000).ease(d3.easeLinear);
  
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
     .attr("y", -40)
     .attr("dy", ".71em")
     .attr("x", -height/2 + 40)
     .attr("dx", ".71em")
     .style("text-anchor", "end")
     .attr("fill", "#5D6971")
     .text("Profit ($)");

  var line_stuff = g.selectAll(".line")
      .data([data]);

  line_stuff.enter().append("path").classed("line", true)
             .merge(line_stuff);

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


  g.selectAll(".line")
    .transition()
    .duration(10000)
    .ease(d3.easeLinear)
    .attr("d", line);

  $(document).ready(function() {
    $("button#calculate").click(function() {
      let metrics = get_metrics();
      send_metrics(metrics);
      })
    })

};

let send_metrics = function(metrics) {
  $.ajax({
    url: '/generate',
    contentType: "application/json; charset=utf-8",
    type: 'POST',
    data: JSON.stringify(metrics),
    success: function(data) {
      draw(data);
    }
  });
};