"use strict";
var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 33.746511, lng: -84.388339}, 
    zoom: 9
  });
  var green_square = {
    path: 'M -2,-2 2,-2 2,2 -2,2 z',
    strokeColor: '#00e600',
    strokeOpacity: .4,
    fillColor: '#00e600',
    fillOpacity: .4,
    scale: 1
  };
  var grey_square = {
    path: 'M -2,-2 2,-2 2,2 -2,2 z',
    strokeColor: '#999999',
    strokeOpacity: .6,
    fillColor: '#999999',
    fillOpacity: .6,
    scale: 1
  };
  $.getJSON("../static/data/lat_long.json", function(d) {
  for (var i = 0; i < d.length; i++) {
      var marker = new google.maps.Marker({
      position: {lat: d[i]["Latitude"],
                 lng: d[i]["Longitude"]},
      map: map,
      icon: (d[i]["Status"] === 1) ? green_square : grey_square,
      title: 'Hello World!'
      }); 
    }
  });
}