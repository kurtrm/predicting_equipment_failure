"use strict";
var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('mapblock'), {
    center: {lat: 33.746511, lng: -84.388339}, 
    zoom: 9
  });
  var centerControlDiv = document.createElement('div');
  var centerControl = new CenterControl(centerControlDiv, map);
  centerControlDiv.index = 1;
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerControlDiv);
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
      icon: (d[i]["Status"] === 1) ? green_square : grey_square
      // title: 'Hello World!'
      }); 
    }
  });
}

   /**
       * The CenterControl adds a control to the map that recenters the map on
       * Chicago.
       * This constructor takes the control DIV as an argument.
       * @constructor
       */
function CenterControl(controlDiv, map) {

  // Set CSS for the control border.
  var controlUI = document.createElement('div');
  controlUI.style.backgroundColor = '#fff';
  controlUI.style.border = '2px solid #fff';
  controlUI.style.borderRadius = '3px';
  controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
  controlUI.style.cursor = 'pointer';
  controlUI.style.marginBottom = '22px';
  controlUI.style.textAlign = 'center';
  controlUI.title = 'Click to recenter the map';
  controlDiv.appendChild(controlUI);

  // Set CSS for the control interior.
  var controlText = document.createElement('div');
  controlText.style.color = 'rgb(25,25,25)';
  controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
  controlText.style.fontSize = '16px';
  controlText.style.lineHeight = '38px';
  controlText.style.paddingLeft = '5px';
  controlText.style.paddingRight = '5px';
  controlText.innerHTML = ' Center S. GA';
  controlUI.appendChild(controlText);

  // Setup the click event listeners: simply set the map to Chicago.
  var flag = true
  controlUI.addEventListener('click', function() {
    if (flag) {
      map.setCenter({lat: 31.232117, lng: -84.210631});
      controlText.innerHTML = 'Center ATL'
      flag = false;
    } else {
    map.setCenter({lat: 33.746511, lng: -84.388339});
    flag = true;
  };
  });

}
