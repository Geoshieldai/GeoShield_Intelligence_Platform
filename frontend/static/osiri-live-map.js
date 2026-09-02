/* GeoShield OS - OSIRI Fullscreen High-Res Satellite Engine */
(function () {
    "use strict";

    let liveMap = null;

    function initOsiriMap() {
        const mapContainer = document.getElementById("osiriFullscreenMap");
        if (!mapContainer) return;

        if (!liveMap) {
            // Esri High-Resolution Satellite Base Layer
            const satelliteTileLayer = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
                attribution: "Tiles &copy; Esri, Maxar, Earthstar Geographics &mdash; GeoShield OSIRI Satellite",
                maxZoom: 19,
                maxNativeZoom: 18
            });

            // Tactical Dark Overlay for Labels & Borders
            const referenceLabels = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}", {
                attribution: "",
                maxZoom: 19
            });

            liveMap = L.map("osiriFullscreenMap", {
                center: [-1.286389, 36.817223],
                zoom: 7,
                layers: [satelliteTileLayer, referenceLabels]
            });

            loadCameraMarkers();
        }

        setTimeout(() => { if (liveMap) liveMap.invalidateSize(); }, 200);
    }

    async function loadCameraMarkers() {
        try {
            const res = await fetch("/api/osiri/cameras");
            const data = await res.json();
            if (!data || !data.cameras) return;

            data.cameras.forEach(cam => {
                // High-visibility pulse marker over satellite imagery
                const marker = L.circleMarker([cam.lat, cam.lng], {
                    radius: 9,
                    fillColor: "#22c55e", // Neon Green for high satellite contrast
                    color: "#ffffff",
                    weight: 2,
                    fillOpacity: 1.0
                }).addTo(liveMap);

                marker.bindPopup(`
                    <div style="color: #0f172a; font-family: sans-serif; min-width: 210px;">
                        <h4 style="margin: 0 0 4px 0;">📷 ${cam.name}</h4>
                        <p style="margin: 0 0 6px 0; font-size: 11px; color: #475569;">County: ${cam.county} (${cam.resolution})</p>
                        <button onclick="window.openOsiriStream('${cam.name}', '${cam.stream_url}')" style="width: 100%; background: #059669; color: #fff; border: none; padding: 7px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 11px;">
                            🎥 Open Satellite Ground Feed
                        </button>
                    </div>
                `);
            });
        } catch (err) {
            console.error("OSIRI cameras fetch error:", err);
        }
    }

    window.openOsiriLiveMap = function() {
        const liveMapSection = document.getElementById("osiriLiveMapPage");
        const defaultMap = document.getElementById("geoshieldMapPage") || document.querySelector("main > section:first-of-type");
        
        if (liveMapSection) {
            if (defaultMap && defaultMap !== liveMapSection) defaultMap.style.display = "none";
            liveMapSection.style.display = "block";
            initOsiriMap();
        }
    };

    window.closeOsiriLiveMap = function() {
        const liveMapSection = document.getElementById("osiriLiveMapPage");
        const defaultMap = document.getElementById("geoshieldMapPage") || document.querySelector("main > section:first-of-type");
        
        if (liveMapSection) liveMapSection.style.display = "none";
        if (defaultMap) defaultMap.style.display = "block";
    };

    window.openOsiriStream = function(name, url) {
        const modal = document.getElementById("osiriStreamModal");
        const title = document.getElementById("osiriStreamTitle");
        const player = document.getElementById("osiriVideoPlayer");
        if (modal && title && player) {
            title.textContent = name;
            player.src = url;
            modal.style.display = "flex";
            player.play().catch(() => {});
        }
    };

    window.closeOsiriStream = function() {
        const modal = document.getElementById("osiriStreamModal");
        const player = document.getElementById("osiriVideoPlayer");
        if (modal) modal.style.display = "none";
        if (player) player.pause();
    };

    window.toggleOsiriHistory = function() {
        const modal = document.getElementById("osiriHistoryModal");
        if (!modal) return;
        modal.style.display = modal.style.display === "flex" ? "none" : "flex";
        if (modal.style.display === "flex") window.loadOsiriRecordings();
    };

    window.loadOsiriRecordings = async function() {
        const dateVal = document.getElementById("osiriHistoryDate")?.value || "";
        const list = document.getElementById("osiriRecordingsList");
        if (!list) return;

        list.innerHTML = "<div style='color: #94a3b8;'>Loading 24h recordings...</div>";

        try {
            const res = await fetch(`/api/osiri/recordings${dateVal ? '?date=' + dateVal : ''}`);
            const data = await res.json();
            
            if (!data.recordings || data.recordings.length === 0) {
                list.innerHTML = "<div style='color: #94a3b8;'>No recordings found for selected date.</div>";
                return;
            }

            list.innerHTML = data.recordings.map(rec => `
                <div style="background: #020617; border: 1px solid #1e293b; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="font-weight: bold; color: #38bdf8; font-size: 13px;">📼 ${rec.filename}</div>
                        <div style="font-size: 11px; color: #64748b;">Date: ${rec.date} | Duration: ${rec.duration} | Size: ${rec.size}</div>
                    </div>
                    <button onclick="window.openOsiriStream('${rec.filename}', 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4')" style="background: #059669; color: #fff; border: none; padding: 6px 12px; border-radius: 4px; font-size: 11px; cursor: pointer; font-weight: bold;">
                        ▶ Replay
                    </button>
                </div>
            `).join("");
        } catch (err) {
            list.innerHTML = "<div style='color: #ef4444;'>Failed to load archives.</div>";
        }
    };

    document.addEventListener("click", function (e) {
        const target = e.target.closest("a, button, li");
        if (target && target.innerText && target.innerText.includes("Live Map")) {
            e.preventDefault();
            window.openOsiriLiveMap();
        }
    });
})();
