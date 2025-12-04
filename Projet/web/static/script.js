const mapEl = document.getElementById('map');
const center = [46.9131, -71.2085]; // 10km north of Quebec City

const map = L.map('map').setView(center, 15);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap'
}).addTo(map);

let droneMarkers = {};
let droneCircles = {};
let cowMarkers = {};
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
    console.log('API Response:', data);
    
    const drones = data.drones || [];
    const cows = data.cows || [];

    console.log(`Received: ${drones.length} drones, ${cows.length} cows`);

    // Update drone markers
    const dronesSeen = new Set();
    drones.forEach((d, idx) => {
      dronesSeen.add(d.id);
      if (!droneMarkers[d.id]) {
        console.log(`Creating drone marker ${idx}: ${d.id} at [${d.lat}, ${d.lng}]`);
        droneMarkers[d.id] = L.marker([d.lat, d.lng], {
          icon: L.divIcon({
            html: '🚁',
            className: 'drone-icon',
            iconSize: [24, 24]
          })
        }).addTo(map).bindPopup(`Drone ${d.id}<br>Lat: ${d.lat.toFixed(6)}<br>Lng: ${d.lng.toFixed(6)}`);
      } else {
        droneMarkers[d.id].setLatLng([d.lat, d.lng]);
      }
      
      if (!droneCircles[d.id]) {
        droneCircles[d.id] = L.circle([d.lat, d.lng], {
          radius: d.radius || 500, 
          color: 'blue', 
          fillOpacity: 0.1,
          weight: 2
        }).addTo(map);
      } else {
        droneCircles[d.id].setLatLng([d.lat, d.lng]);
        droneCircles[d.id].setRadius(d.radius || 500);
      }
    });

    // Update cow markers  
    const cowsSeen = new Set();
    cows.forEach(cow => {
      cowsSeen.add(cow.id);
      const isOutside = cow.outside_zone;
      const cowIcon = isOutside ? '🐄💨' : '🐄'; // Different icon for cows outside zone
      
      if (!cowMarkers[cow.id]) {
        cowMarkers[cow.id] = L.marker([cow.lat, cow.lng], {
          icon: L.divIcon({
            html: cowIcon,
            className: `cow-icon ${isOutside ? 'cow-outside' : 'cow-inside'}`,
            iconSize: [16, 16]
          })
        }).addTo(map).bindPopup(`Vache ${cow.id} ${isOutside ? '(Hors zone)' : '(Dans la zone)'}`);
      } else {
        cowMarkers[cow.id].setLatLng([cow.lat, cow.lng]);
        cowMarkers[cow.id].setIcon(L.divIcon({
          html: cowIcon,
          className: `cow-icon ${isOutside ? 'cow-outside' : 'cow-inside'}`,
          iconSize: [16, 16]
        }));
      }
    });

    // Remove stale markers
    Object.keys(droneMarkers).forEach(id => { 
      if (!dronesSeen.has(id)) { 
        map.removeLayer(droneMarkers[id]); 
        delete droneMarkers[id]; 
      } 
    });
    Object.keys(droneCircles).forEach(id => { 
      if (!dronesSeen.has(id)) { 
        map.removeLayer(droneCircles[id]); 
        delete droneCircles[id]; 
      } 
    });
    Object.keys(cowMarkers).forEach(id => { 
      if (!cowsSeen.has(id)) { 
        map.removeLayer(cowMarkers[id]); 
        delete cowMarkers[id]; 
      } 
    });

    // Draw surveillance zone polygon
    if (hullLayer) { map.removeLayer(hullLayer); hullLayer = null; }
    if (data.hull && data.hull.length > 2) {
      const latlngs = data.hull.map(p => [p.lat, p.lng]);
      hullLayer = L.polygon(latlngs, {
        color: 'orange', 
        fillColor: 'yellow',
        fillOpacity: 0.2,
        weight: 3,
        dashArray: '5, 10'
      }).addTo(map);
    }

    // Update charts
    if (data.timeseries) {
      updateCharts(data.timeseries.t, data.timeseries.in, data.timeseries.out);
    }
  }).catch(err => console.error('state fetch', err));
}

// initial load
fetchState();
setInterval(fetchState, 1500);
