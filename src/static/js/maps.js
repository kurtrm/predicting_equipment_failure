"use strict";
var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 33.746511, lng: -84.388339}, 
    zoom: 9
  });
  var square = {
    path: 'M -2,-2 2,-2 2,2 -2,2 z',
    strokeColor: '#006699',
    strokeOpacity: .3,
    fillColor: '#006699',
    fillOpacity: .3,
    scale: 1
  };
  $.getJSON("../static/data/lat_long.json", function(d){
  for (var i = 0; i < d.length; i++) {
      var marker = new google.maps.Marker({
      position: {lat: d[i]["Latitude"],
                 lng: d[i]["Longitude"]},
      map: map,
      icon: square,
      title: 'Hello World!'
      }); 
    }
  });
}