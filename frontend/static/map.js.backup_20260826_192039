console.log("MAP.JS VERSION 2 LOADED");
// ======================================================
// GeoShield AI
// Map Module
// ======================================================

function initializeMap() {

    // Layers
    window.infrastructureLayer = L.layerGroup();
    window.fireLayer = L.layerGroup();
    window.responseLayer = L.layerGroup();

    // Map
    window.map = L.map("map", {
        zoomControl: true
    }).setView([-0.0236, 37.9062], 6);

    // Base Maps
    const satellite = L.tileLayer(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        {
            attribution: "Esri"
        }
    );

    const street = L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution: "© OpenStreetMap"
        }
    );

    const labels = L.tileLayer(
        "https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png",
        {
            attribution: "© CARTO",
            pane: "overlayPane"
        }
    );

    // Default layers
    satellite.addTo(map);
    labels.addTo(map);

    fireLayer.addTo(map);
    responseLayer.addTo(map);
    infrastructureLayer.addTo(map);

    // Layer Control
    L.control.layers(
        {
            "🛰 Satellite": satellite,
            "🛣 Street": street
        },
        {
            "🔥 Fire Hotspots": fireLayer,
            "🏥 Resources": infrastructureLayer,
            "🚑 Response Route": responseLayer
        },
        {
            collapsed: false
        }
    ).addTo(map);

    console.log("✅ Map initialized");
}