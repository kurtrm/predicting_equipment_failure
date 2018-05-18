"use strict";
(function(window, document) {
// I leaned heavily on D3 documentation and lots of examples to generate this code.

  var svg = d3.select("svg#precision_recall"),
      margin = {top: 20, right: 40, bottom: 30, left: -15},
      width = +svg.attr("width") - 50 - margin.left - margin.right,
      height = +svg.attr("height") - margin.top - margin.bottom;

  var x = d3.scaleLinear()
      .range([0, width]);

  var y = d3.scaleLinear()
      .range([height, 0]);

  var line1 = d3.line()
      .x(d => x(d.recall))
      .y(d => y(d.precision));

  var g = svg.append("g")
      .attr("transform", "translate(" + (margin.left + 50) + "," + margin.top + ")");

  d3.json("/precision_recall", function(thisData) {

    x.domain([0, d3.max(thisData, d => d.recall)]);
    y.domain([0, d3.max(thisData, d => d.precision)]);

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
       .text("Recall");


    g.append("g")
        .attr("class", "axis axis--y")
        .call(d3.axisLeft(y))
     .append("text")
       .attr("class", "axis-title")
       .attr("transform", "rotate(-90)")
       .attr("y", -37)
       .attr("dy", ".91em")
       .attr("x", -height/2 + 40)
       .attr("dx", ".71em")
       .style("text-anchor", "end")
       .attr("fill", "#5D6971")
       .text("Precision");

    var pr_line = g.selectAll(".line")
        .data([thisData]);

    pr_line.enter().append("path").classed("line", true)
             .merge(pr_line)
             .attr("d", line1)
             .attr("fill", "none")
             .attr("stroke", "black")
             .attr("stroke-dasharray", function(d){
              return this.getTotalLength()
             })
             .attr("stroke-dashoffset", function(d){
              return this.getTotalLength()
             });

    g.append("text")
        .attr("class", "average_precision")
        .attr("x", x(.35))
        .attr("dx", "2em")
        .attr("y", y(1.05))
        .style("text-anchor", "end")
        .style("font-size", "12px")
        .text("Average precision: .837");

    g.selectAll(".line")
      .transition()
      .duration(1000)
      .ease(d3.easeLinear)
      .attr("stroke-dashoffset", 0);

  /* Javascript function declaration. Hoisted.
  Javascript functions can also be expressions, where they're put into
  variable. They are not hoisted. */

  });
})(window, document);