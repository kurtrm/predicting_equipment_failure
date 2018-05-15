"use strict";
// I leaned heavily on D3 documentation and lots of examples to generate this code.

var bisect = d3.bisector((d) => d.fpr).right;

var svg = d3.select("svg"),
    margin = {top: 20, right: 20, bottom: 30, left: 20},
    width = +svg.attr("width") - 400 - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;

var x = d3.scaleLinear()
    .range([0, width]);

var y = d3.scaleLinear()
    .range([height, 0]);

var line1 = d3.line()
    .x(d => x(d.fpr))
    .y(d => y(d.tpr));

var invisline1 = d3.line()
    .x(d => x(d.fpr))
    .y(d => y(d.tpr));

var line2 = d3.line()
    .x(d => x(d.lin))
    .y(d => y(d.lin));

var g = svg.append("g")
    .attr("transform", "translate(" + (margin.left + 50) + "," + margin.top + ")");

d3.json("static/data/roc_data.json", function(thisData) {

  x.domain([0, d3.max(thisData, d => d.fpr)]);
  y.domain([0, d3.max(thisData, d => d.tpr)]);

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
     .text("False Positive Rate (FPR)");


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
     .text("True Positive Rate (TPR)");

  g.append("path")
      .datum(thisData)
      .attr("class", "line")
      .attr("d", line1);

  g.append("path")
      .datum(thisData)
      .attr("class", "hiddenLine")
      .attr("d", invisline1)
      .on("mouseover", function() { focus.style("display", null); })
      .on("mouseout", function() { focus.style("display", "none"); })
      .on("mousemove", mousemove);

  g.append("path")
      .datum(thisData)
      .attr("class", "line2")
      .style("stroke-dasharray", ("3, 3"))
      .attr("d", line2);

  var focus = g.append("g")
      .attr("class", "focus")
      .style("display", "none");

  focus.append("circle")
      .attr("r", 5);

  focus.append("text")
      .attr("x", 10)
      .attr("dy", ".31em")
     .attr("height", height)

/* Javascript function declaration. Hoisted.
Javascript functions can also be expressions, where they're put into
variable. They are not hoisted. */
  function mousemove() {
      var x0 = x.invert(d3.mouse(this)[0]),
          i = bisect(thisData, x0, 1),
          d0 = thisData[i - 1],
          d1 = thisData[i],
          d = x0 - d0.fpr > d1.fpr - x0 ? d1: d0;
      focus.attr("transform", "translate(" + x(d.fpr) + "," + y(d.tpr) + ")");

      focus.select("text").text(() => Math.round(d.fpr * 100) / 100);

      $("#TP").html = d.fpr;
      $("#FP").html = d.fpr;
      $("#TN").html = d.fpr;
      $("#FN").html = d.fpr;
  }

});