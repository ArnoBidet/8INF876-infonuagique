const mapEl = document.getElementById('map');
const center = [46.8139, -71.2080];

const map = L.map('map').setView(center, 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap'
}).addTo(map);

let droneMarkers = {};
let droneCircles = {};
let hullLayer = null;

// Charts
const ctxIn = document.getElementById('chartIn').getContext('2d');
const ctxOut = document.getElementById('chartOut').getContext('2d');

const chartIn = new Chart(ctxIn, {
  type: 'line',
  data: { labels: [], datasets: [{ label: 'In Zone', data: [], borderColor: 'green', fill:false }] },
  options: { scales: { x: { display: true } } }
});

const chartOut = new Chart(ctxOut, {
  type: 'line',
  data: { labels: [], datasets: [{ label: 'Out Zone', data: [], borderColor: 'red', fill:false }] },
  options: { scales: { x: { display: true } } }
});

function updateCharts(times, ins, outs) {
  const labels = times.map(t => new Date(t*1000).toLocaleTimeString());
  chartIn.data.labels = labels; chartIn.data.datasets[0].data = ins; chartIn.update();
  chartOut.data.labels = labels; chartOut.data.datasets[0].data = outs; chartOut.update();
}

function fetchState() {
  fetch('/api/state').then(r => r.json()).then(data => {
    const drones = data.drones;

    // update markers
    const seen = new Set();
    drones.forEach(d => {
      seen.add(d.id);
      if (!droneMarkers[d.id]) {
        droneMarkers[d.id] = L.marker([d.lat, d.lng]).addTo(map).bindPopup(d.id);
      } else {
        droneMarkers[d.id].setLatLng([d.lat, d.lng]);
      }
      if (!droneCircles[d.id]) {
        droneCircles[d.id] = L.circle([d.lat, d.lng], {radius: d.radius, color: 'blue', opacity:0.3}).addTo(map);
      } else {
        droneCircles[d.id].setLatLng([d.lat, d.lng]);
        droneCircles[d.id].setRadius(d.radius);
      }
    });

    // remove stale markers
    Object.keys(droneMarkers).forEach(id => { if (!seen.has(id)) { map.removeLayer(droneMarkers[id]); delete droneMarkers[id]; } });
    Object.keys(droneCircles).forEach(id => { if (!seen.has(id)) { map.removeLayer(droneCircles[id]); delete droneCircles[id]; } });

    // draw hull polygon
    if (hullLayer) { map.removeLayer(hullLayer); hullLayer = null; }
    if (data.hull && data.hull.length > 0) {
      const latlngs = data.hull.map(p => [p.lat, p.lng]);
      hullLayer = L.polygon(latlngs, {color: 'orange', fillOpacity: 0.1}).addTo(map);
    }

    // update charts
    if (data.timeseries) {
      updateCharts(data.timeseries.t, data.timeseries.in, data.timeseries.out);
    }
  }).catch(err => console.error('state fetch', err));
}

// initial load
fetchState();
setInterval(fetchState, 1500);
