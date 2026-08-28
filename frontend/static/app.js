
/*
============================================================
 Sentinel-2 Frontend Initialization
============================================================
*/

function initializeSentinel2Safe() {

    try {

        if (
            window.Sentinel2 &&
            typeof window.Sentinel2.initialize === "function"
        ) {

            window.Sentinel2.initialize();

            console.log(
                "GeoShield Sentinel-2 frontend initialized."
            );

        }
        else {

            console.warn(
                "Sentinel-2 module loaded, but initialize() was not found."
            );

        }

    }
    catch (error) {

        console.error(
            "Sentinel-2 initialization failed:",
            error
        );

    }

}

// ======================================================
// GeoShield AI
// Main Entry Point
// ======================================================
console.log(typeof initializeMap);

initializeMap();

loadCounties();


// Auto Refresh

setInterval(loadDashboard, 60000);

setInterval(loadFireHotspots, 30000);



document.addEventListener(
    "DOMContentLoaded",
    initializeSentinel2Safe
);

