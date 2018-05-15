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

d3.json("/retrieve_profit_curve", function(thisData) {
  draw(thisData);
});

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

  g.append("text")
      .attr("class", "max_thresh")
      .attr("x", x(x_val))
      .attr("dx", "2em")
      .attr("y", y(y_max))
      .style("text-anchor", "end")
      .text(Math.round(x_val * 100) / 100);


  g.selectAll(".line")
    .transition()
    .duration(10000)
    .ease(d3.easeLinear)
    .attr("d", line);

};

$(document).ready(function() {
  $("button#calculate").click(function() {
    $(".assess-box").children("button").remove();
    $("p#assessment").text("Loading...")
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
      statement();
    }
  });
}

let get_metrics = function() {
  let revenue = $("input#revenue").val()
  let maintenance = $("input#maintenance").val()
  let repair = $("input#repair").val()
  return {"user_input": [revenue, maintenance, repair]}
};

function statement() {
  var threshold = $("text.max_thresh").text();
  var threshold_statement = threshold + " is the optimal threshold for the given revenue, maintenance, and repair costs. Would you like to save this threshold?"
  $("p#assessment").text(threshold_statement)
  var cancel = $('<button type="button" class="btn btn-danger id=cancel">Cancel</button>').click(function() {
    console.log("I heard you click cancel.");
    $(".assess-box").empty().append('<p id="assessment"></p>')
  });
  var save = $('<button type="button" class="btn btn-success id=save">Save</button>').click(function() {
    $.ajax({
      url: '/save_profit_curve',
      contentType: "application/json; charset=utf-8",
      type: 'POST',
      data: JSON.stringify(threshold),
      success: function() {
        location.reload();
      }
    })
  });
  $(".assess-box").append(cancel).append(save)
}