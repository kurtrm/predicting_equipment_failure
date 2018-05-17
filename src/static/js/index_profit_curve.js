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
  var threshold = JSON.parse(localStorage["threshold"]);
  var cost = JSON.parse(localStorage["cost"]);
  var metrics = JSON.parse(localStorage["metrics"]);
  var time = JSON.parse(localStorage["rightNow"]);
  var revenue = metrics["user_input"][0];
  var maintenance = metrics["user_input"][1];
  var repair = metrics["user_input"][2];
  $("#threshold").html("0." + threshold);
  $("#cost").html("-$" + -cost);
  $("#revenue").html(revenue);
  $("#maintenance").html("-$" + -maintenance);
  $("#repair").html("-$" + -repair);
  $("#time").html(time);
  draw(storage);
};

function draw(data) {
  $("svg#profit_curve").empty()
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

};
})(window, document);