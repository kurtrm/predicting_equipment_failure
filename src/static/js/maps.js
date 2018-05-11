"use strict";
var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 33.746511, lng: -84.388339}, 
    zoom: 8
  });
  $.getJSON("../static/data/lat_long.json", function(d){
  for (var i = 0; i < d.length; i++) {
      var marker = new google.maps.Marker({
      position: {lat: d[i]["Latitude"],
                 lng: d[i]["Longitude"]},
      map: map,
      title: 'Hello World!'
      }); 
    }
  });
}