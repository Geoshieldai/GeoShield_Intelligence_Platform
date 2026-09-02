// ======================================================
// GeoShield AI
// Counties Module
// ======================================================

function loadCounties() {

    fetch("/static/data/kenya_counties.geojson")

        .then(response => response.json())

        .then(data => {

            L.geoJSON(data, {

                style: function (feature) {

                    const risk = Number(feature.properties.Drought_Risk || 0);

                    let fill = "#00b894";

                    if (risk >= 30) fill = "#f1c40f";
                    if (risk >= 50) fill = "#e67e22";
                    if (risk >= 70) fill = "#e74c3c";

                    return {

                        color: "#55ffff",
                        weight: 1,
                        fillColor: fill,
                        fillOpacity: 0.30

                    };

                },

                onEachFeature: function (feature, layer) {

                    const county =

                        feature.properties.COUNTY ||

                        feature.properties.NAME ||

                        feature.properties.name ||

                        "Unknown";

                    layer.on({

                        mouseover: function (e) {

                            e.target.setStyle({

                                weight: 3,
                                color: "#00ff88",
                                fillOpacity: 0.45

                            });

                        },

                        mouseout: function (e) {

                            e.target.setStyle({

                                weight: 1,
                                color: "#55ffff",
                                fillOpacity: 0.30

                            });

                        },

                        click: function () {

                            // Save current county globally

                            window.currentCounty = county;

                            // Zoom to county

                            window.map.fitBounds(layer.getBounds(), {

                                padding: [20, 20],
                                maxZoom: 10

                            });

                            // Load nearby infrastructure

                            loadInfrastructure(county);

                            // Load county statistics

                            fetch("/county/" + encodeURIComponent(county))

                                .then(response => response.json())

                                .then(info => {

                                    layer.bindPopup(`

<b>${info.County}</b>

<hr>

🌧️ Rainfall: ${Number(info.Rainfall_mm).toFixed(0)} mm<br>

🌡️ Temperature: ${Number(info.Temperature_C).toFixed(1)} °C<br>

🌿 NDVI: ${Number(info.NDVI).toFixed(2)}<br>

🚨 Drought Risk: ${Number(info.Drought_Risk).toFixed(1)}%

`).openPopup();

                                    // -----------------------
                                    // Right Panel
                                    // -----------------------

                                    document.getElementById("weather").innerText =
                                        Number(info.Temperature_C).toFixed(1) + "°C";

                                    // -----------------------
                                    // Bottom Dashboard
                                    // -----------------------

                                    document.getElementById("ndviCard").innerText =
                                       formatNumber(info.NDVI)

                                    document.getElementById("rainfallCard").innerText =
                                        Number(info.Rainfall_mm).toFixed(0) + " mm";

                                    document.getElementById("temperatureCard").innerText =
                                        formatNumber(info.Temperature_C, 1)

                                    const flood = getFloodRisk(info.Rainfall_mm);

                                    document.getElementById("floodRiskCard").innerText =
                                        flood;

                                    const fire = getFireRisk(info.Drought_Risk);

                                    document.getElementById("fireRisk").innerText =
                                        fire;

                                    document.getElementById("fireRiskCard").innerText =
                                        fire;

                                    document.getElementById("populationCard").innerText =
                                        info.Population || "N/A";

                                })

                                .catch(console.error);

                        }

                    });

                }

            }).addTo(map);

        })

        .catch(console.error);

}
