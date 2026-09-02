(function () {

    "use strict";

    /*
    ============================================================
    GEOSHIELD AI ENTERPRISE
    SATELLITE HORIZONTAL NAVIGATOR
    ============================================================

    RESPONSIBILITY:

        The actual satellite card movement is owned by
        satellites.js.

        This file MUST NOT:
        - use scrollBy()
        - modify scrollLeft
        - attach competing click handlers
        - move the document
        - move the workspace
        - affect Sentinel-2

        satellites.js owns:
            moveSatelliteTrack(-1)
            moveSatelliteTrack(1)
            transform-based movement
    ============================================================
    */

    const LEFT_BUTTON_ID = "satelliteNavLeft";
    const RIGHT_BUTTON_ID = "satelliteNavRight";

    function updateButtonState() {

        const leftButton =
            document.getElementById(LEFT_BUTTON_ID);

        const rightButton =
            document.getElementById(RIGHT_BUTTON_ID);

        if (!leftButton || !rightButton) {
            return;
        }

        /*
        --------------------------------------------------------
        satellites.js owns the actual position.
        We only mirror its state here.
        --------------------------------------------------------
        */

        if (
            typeof window.GeoShieldSatelliteNavigatorState
            === "function"
        ) {

            const state =
                window.GeoShieldSatelliteNavigatorState();

            if (state) {

                leftButton.disabled =
                    !state.canMoveLeft;

                rightButton.disabled =
                    !state.canMoveRight;

            }

        }

    }


    function initialize() {

        /*
        IMPORTANT:
        Do NOT bind click events here.

        satellites.js already owns:

            satelliteNavLeft  -> moveSatelliteTrack(-1)
            satelliteNavRight -> moveSatelliteTrack(1)

        Adding another handler here creates competing
        navigation systems.
        */

        updateButtonState();

        console.log(
            "GeoShield Satellite Horizontal Navigator: READY"
        );

    }


    window.GeoShieldSatelliteNavigator = {

        initialize: initialize,

        update: updateButtonState

    };


    if (
        document.readyState === "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            initialize,
            { once: true }
        );

    } else {

        initialize();

    }

})();
