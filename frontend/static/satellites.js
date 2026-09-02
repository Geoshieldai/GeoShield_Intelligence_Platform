/* GeoShield OS - Satellite Workspace Controller */
(function () {
    "use strict";

    const DEFAULT_SATELLITES = [
        {
            id: "osiri",
            name: "OSIRI",
            provider: "GeoShield OSINT Engine",
            category: "REAL-TIME & LIVE INTELLIGENCE",
            description: "Open Source Intelligence & Real-Time Observation Engine combining orbital tracking, live feeds, and space-based intelligence.",
            status: "active",
            capabilities: ["Live Camera Feeds", "Orbital Tracking", "OSINT Fusion", "Starlink Tracking", "Real-Time Analysis"]
        },
        {
            id: "sentinel2",
            name: "Sentinel-2",
            provider: "Copernicus Data Space",
            category: "OPTICAL MULTISPECTRAL",
            description: "Multispectral Earth observation imagery for vegetation, agriculture, fire and environmental intelligence.",
            status: "active",
            capabilities: ["True Color", "NDVI", "NDWI", "NBR", "Agriculture", "Fire Analysis", "Change Detection"]
        },
        {
            id: "sentinel1",
            name: "Sentinel-1",
            provider: "Copernicus Data Space",
            category: "SAR RADAR",
            description: "Synthetic Aperture Radar imagery for flood mapping, surface monitoring and all-weather Earth observation.",
            status: "planned",
            capabilities: ["Flood Detection", "Surface Monitoring", "Change Detection", "SAR Analysis"]
        },
        {
            id: "viirs",
            name: "VIIRS",
            provider: "NASA / NOAA",
            category: "THERMAL / ENVIRONMENTAL",
            description: "Near-real-time environmental observations for fire, thermal anomalies and atmospheric monitoring.",
            status: "planned",
            capabilities: ["Fire Hotspots", "Thermal Anomalies", "Nighttime Lights", "Environmental Monitoring"]
        },
        {
            id: "gpm",
            name: "GPM",
            provider: "NASA",
            category: "PRECIPITATION",
            description: "Global precipitation observations for rainfall monitoring and flood intelligence.",
            status: "planned",
            capabilities: ["Rainfall", "Precipitation", "Flood Intelligence"]
        },
        {
            id: "era5",
            name: "ERA5",
            provider: "ECMWF / Copernicus",
            category: "CLIMATE / WEATHER",
            description: "Global atmospheric reanalysis data for weather, climate and environmental intelligence.",
            status: "planned",
            capabilities: ["Temperature", "Wind", "Pressure", "Humidity"]
        }
    ];

    function renderSatellites(satellites) {
        const grid = document.getElementById("satelliteGrid");
        const statusEl = document.getElementById("satelliteSystemStatus");
        if (!grid) return;

        const activeCount = satellites.filter(s => s.status === "active").length;
        if (statusEl) {
            statusEl.textContent = `${activeCount} active / ${satellites.length} registered`;
        }

        grid.innerHTML = satellites.map(s => {
            const isActive = s.status === "active";
            const badgeText = isActive ? "ACTIVE" : "PLANNED";
            
            const capsHtml = (s.capabilities || []).map(c => 
                `<span style="background:#1e293b; color:#94a3b8; font-size:11px; padding:3px 8px; border-radius:4px; margin-right:4px; margin-bottom:4px; display:inline-block;">${c}</span>`
            ).join("");

            const btnHtml = isActive
                ? `<button type="button" class="satellite-open-btn" data-satellite-id="${s.id}" style="width:100%; margin-top:16px; background:#2563eb; color:#fff; border:none; padding:10px; border-radius:6px; cursor:pointer; font-weight:600; transition:background 0.2s;">Open Satellite</button>`
                : `<button type="button" class="satellite-open-btn planned" disabled style="width:100%; margin-top:16px; background:#1e293b; color:#64748b; border:none; padding:10px; border-radius:6px; cursor:not-allowed;">Coming Soon</button>`;

            return `
                <div class="satellite-card" data-satellite="${s.id}" style="flex:0 0 340px; min-width:340px; background:#0f172a; border:1px solid #1e293b; border-radius:12px; padding:20px; display:flex; flex-direction:column; justify-content:space-between; box-sizing:border-box;">
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                            <div>
                                <h3 style="margin:0; color:#f8fafc; font-size:18px;">${s.name}</h3>
                                <span style="color:#64748b; font-size:12px;">${s.provider}</span>
                            </div>
                            <span style="font-size:10px; font-weight:700; padding:2px 8px; border-radius:10px; background:${isActive ? 'rgba(34,197,94,0.15)' : 'rgba(234,179,8,0.15)'}; color:${isActive ? '#4ade80' : '#facc15'}; border:1px solid ${isActive ? 'rgba(34,197,94,0.3)' : 'rgba(234,179,8,0.3)'};">${badgeText}</span>
                        </div>
                        <div style="color:#38bdf8; font-size:11px; font-weight:700; letter-spacing:0.5px; margin-bottom:8px;">${s.category}</div>
                        <p style="color:#94a3b8; font-size:13px; line-height:1.4; margin-bottom:12px;">${s.description}</p>
                        <div style="display:flex; flex-wrap:wrap;">${capsHtml}</div>
                    </div>
                    ${btnHtml}
                </div>
            `;
        }).join("");
    }

    async function loadSatellites() {
        try {
            const res = await fetch("/satellites");
            if (!res.ok) throw new Error("API not ready");
            const data = await res.json();
            if (data && Array.isArray(data.satellites) && data.satellites.length > 0) {
                const hasOsiri = data.satellites.some(s => s.id === "osiri");
                const list = hasOsiri ? data.satellites : [DEFAULT_SATELLITES[0], ...data.satellites];
                renderSatellites(list);
                return;
            }
        } catch (err) {
            console.log("Using built-in satellite cards registry.");
        }
        renderSatellites(DEFAULT_SATELLITES);
    }

    function setupCloseBtn(productSec) {
        let header = productSec.querySelector("[class*='-header']") || productSec.firstElementChild;
        if (header && !header.querySelector(".sat-close-btn")) {
            const closeBtn = document.createElement("button");
            closeBtn.type = "button";
            closeBtn.className = "sat-close-btn";
            closeBtn.innerHTML = "&#10005;";
            closeBtn.title = "Close Satellite View";
            closeBtn.style.cssText = "background:#ef4444; color:#ffffff; border:none; font-size:16px; width:34px; height:34px; border-radius:50%; cursor:pointer; margin-left:auto; display:inline-flex; align-items:center; justify-content:center; flex-shrink:0; font-weight:bold; box-shadow:0 2px 8px rgba(0,0,0,0.4); transition:background 0.2s;";
            closeBtn.onmouseover = () => closeBtn.style.background = "#dc2626";
            closeBtn.onmouseout = () => closeBtn.style.background = "#ef4444";
            
            header.style.display = "flex";
            header.style.alignItems = "center";
            header.appendChild(closeBtn);
        }
    }

    // Global Event Delegation Logic
    document.addEventListener("click", function (e) {
        if (e.target.closest("#satelliteNavLeft")) {
            e.preventDefault();
            const container = document.getElementById("satelliteGridViewport") || document.getElementById("satelliteGrid");
            if (container) container.scrollBy({ left: -400, behavior: "smooth" });
            return;
        }

        if (e.target.closest("#satelliteNavRight")) {
            e.preventDefault();
            const container = document.getElementById("satelliteGridViewport") || document.getElementById("satelliteGrid");
            if (container) container.scrollBy({ left: 400, behavior: "smooth" });
            return;
        }

        // Open Satellite Click (Dynamic satId)
        const openBtn = e.target.closest(".satellite-open-btn");
        if (openBtn && !openBtn.disabled) {
            e.preventDefault();
            const satId = openBtn.getAttribute("data-satellite-id") || "sentinel2";
            const productSec = document.getElementById(`${satId}Product`) || document.getElementById("sentinel2Product");
            if (productSec) {
                productSec.style.display = "block";
                setupCloseBtn(productSec);
                productSec.scrollIntoView({ behavior: "smooth", block: "nearest" });
            }
            return;
        }

        // Close Button Click (Relative parent section)
        const closeBtn = e.target.closest(".sat-close-btn");
        if (closeBtn) {
            e.preventDefault();
            const productSec = closeBtn.closest("[id$='Product']") || closeBtn.closest("section");
            if (productSec) productSec.style.display = "none";
            return;
        }
    });

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", loadSatellites);
    } else {
        loadSatellites();
    }
})();
