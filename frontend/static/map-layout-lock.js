(function () {
    "use strict";

    /*
     * ============================================================
     * GEOSHIELD — MAP LAYOUT LOCK
     * ============================================================
     *
     * Purpose:
     *   Protect the Map workspace from unintended layout changes.
     *
     * Important:
     *   This does NOT disable map interaction.
     *   Leaflet panning, zooming, search and controls remain active.
     *
     *   This does NOT affect workspace navigation.
     *
     * Default:
     *   LOCKED
     * ============================================================
     */

    let locked = true;

    function setLocked(value) {
        locked = Boolean(value);

        const mapPage =
            document.getElementById(
                "geoshieldMapPage"
            );

        if (mapPage) {
            mapPage.dataset.layoutLocked =
                locked ? "true" : "false";
        }

        console.log(
            "GeoShield Map Layout:",
            locked ? "LOCKED" : "UNLOCKED"
        );
    }

    function lock() {
        setLocked(true);
    }

    function unlock() {
        setLocked(false);
    }

    function isLocked() {
        return locked;
    }

    function initialize() {
        setLocked(true);

        console.log(
            "GeoShield Map Layout Lock READY — LOCKED"
        );
    }

    window.GeoShieldMapLock = {
        initialize: initialize,
        lock: lock,
        unlock: unlock,
        isLocked: isLocked
    };

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            initialize,
            { once: true }
        );
    } else {
        initialize();
    }

})();
