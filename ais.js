// Simple script to display sample AIS data on a Leaflet map

document.addEventListener('DOMContentLoaded', function () {
  var map = L.map('map').setView([0, 0], 2);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  fetch('ais_sample.json')
    .then(function (response) { return response.json(); })
    .then(function (data) {
      (data.ships || []).forEach(function (ship) {
        if (ship.lat && ship.lon) {
          L.marker([ship.lat, ship.lon])
            .addTo(map)
            .bindPopup(ship.name || ship.mmsi || 'Vessel');
        }
      });
    })
    .catch(function (err) { console.error('Failed to load AIS data', err); });
});
