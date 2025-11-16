# Drone Map Demo (Flask + Leaflet)

Single-page demo application that shows drone positions on a Leaflet map, draws the polygon area between drones and coverage circles, and displays two time-series charts (in-zone / out-of-zone counts).

Features
- Periodically fetches drone positions (can proxy to external drone HTTP endpoints via `DRONE_URLS`).
- Simulates moving entities if no external data provided.
- No database — in-memory time series for charts (bounded history).

Quick start (build & run with Docker):

```bash
# from repository root
cd Projet/web
docker build -t drone-map-demo .
docker run -p 5000:5000 drone-map-demo
# open http://localhost:5000
```

Environment variables
- `DRONE_URLS` (optional): comma-separated URLs that return JSON arrays of drone objects: `{id,lat,lng,radius}`.
- `ENTITIES_COUNT` (optional): number of simulated entities (default: 100)
