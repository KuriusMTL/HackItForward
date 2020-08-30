mapboxgl.accessToken = 'pk.eyJ1IjoibmlraXN1IiwiYSI6ImNrZWdla2NvOTB1MWIyeHVxN3lrZmExb3EifQ._NPc57J623HhSRubXYPcIg';

var coordinates = document.getElementById('coordinates');
var lngLat; 

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v10',
    center: [0, 0],
    zoom: 2
});
 
var marker = new mapboxgl.Marker({
    draggable: true
}).setLngLat([0, 0]).addTo(map);
 
function onDragEnd() {
    lngLat = marker.getLngLat();
}
 
marker.on('dragend', onDragEnd);