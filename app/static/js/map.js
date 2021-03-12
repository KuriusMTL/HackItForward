mapboxgl.accessToken = 'pk.eyJ1IjoibmlraXN1IiwiYSI6ImNrZWdla2NvOTB1MWIyeHVxN3lrZmExb3EifQ._NPc57J623HhSRubXYPcIg';
var coordinates = document.getElementById('map');
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-122.4194, 37.7749],
    zoom: 8
});

map.addControl(
  new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    localGeocoder: coordinatesGeocoder,
    zoom: 4,
    placeholder: 'Try: -40, 170',
    mapboxgl: mapboxgl
  })
);

var coordinatesGeocoder = function (query) {
  // match anything which looks like a decimal degrees coordinate pair
  var matches = query.match(
  /^[ ]*(?:Lat: )?(-?\d+\.?\d*)[, ]+(?:Lng: )?(-?\d+\.?\d*)[ ]*$/i
  );
  if (!matches) {
  return null;
  }

  function coordinateFeature(lng, lat) {
    return {
    center: [lng, lat],
    geometry: {
    type: 'Point',
    coordinates: [lng, lat]
    },
    place_name: 'Lat: ' + lat + ' Lng: ' + lng,
    place_type: ['coordinate'],
    properties: {},
    type: 'Feature'
    };
  }

  var coord1 = Number(matches[1]);
  var coord2 = Number(matches[2]);
  var geocodes = [];

  if (coord1 < -90 || coord1 > 90) {
  // must be lng, lat
    geocodes.push(coordinateFeature(coord1, coord2));
  }

  if (coord2 < -90 || coord2 > 90) {
  // must be lat, lng
    geocodes.push(coordinateFeature(coord2, coord1));
  }

  if (geocodes.length === 0) {
  // else could be either lng, lat or lat, lng
    geocodes.push(coordinateFeature(coord1, coord2));
    geocodes.push(coordinateFeature(coord2, coord1));
  }

  return geocodes;
  };


// var marker = new mapboxgl.Marker({
//         draggable: true
//     })
//     .setLngLat([0, 0])
//     .addTo(map);

// function onDragEnd() {
//     var lngLat = marker.getLngLat();
//     // coordinates.style.display = 'block';
//     // coordinates.innerHTML =
//     // 'Longitude: ' + lngLat.lng + '<br />Latitude: ' + lngLat.lat;
// }

// marker.on('dragend', onDragEnd);
