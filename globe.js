// Display vessel positions on a simple 3D globe using three-globe

// Wait until DOM is ready
document.addEventListener('DOMContentLoaded', function () {
  var container = document.getElementById('globe-container');
  if (!container || !window.Globe) {
    return;
  }
  var world = window.Globe()(container)
    .globeImageUrl('https://unpkg.com/three-globe@2/example/img/earth-dark.jpg')
    .pointLat('lat')
    .pointLng('lon')
    .pointAltitude(0.02)
    .pointColor(function () { return 'red'; })
    .pointLabel(function (d) {
      return d.name || d.mmsi || 'Vessel';
    });

  fetch('ais_sample.json')
    .then(function (resp) { return resp.json(); })
    .then(function (data) {
      world.pointsData(data.ships || []);
    })
    .catch(function (err) { console.error('Failed to load AIS data', err); });
});
