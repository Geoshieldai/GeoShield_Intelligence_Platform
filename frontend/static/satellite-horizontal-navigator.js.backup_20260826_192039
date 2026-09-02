(function () {

    "use strict";


    /*
    ============================================================
    GEOSHIELD AI ENTERPRISE
    SATELLITE HORIZONTAL NAVIGATOR
    ============================================================

    RESPONSIBILITY:

        ONLY move the Satellite Intelligence card viewport
        horizontally.

    NEVER:

        - scroll the document
        - scroll window
        - scroll the main workspace
        - change workspace
        - activate Sentinel-2
        - use anchors
        - use scrollIntoView()
        - use window.scrollTo()
        - use IntersectionObserver()

    ============================================================
    */


    const VIEWPORT_ID =
        "satelliteGridViewport";


    const LEFT_BUTTON_ID =
        "satelliteNavLeft";


    const RIGHT_BUTTON_ID =
        "satelliteNavRight";


    let initialized = false;


    /*
    ============================================================
    ELEMENT LOOKUP
    ============================================================
    */

    function getElements() {

        return {

            viewport:
                document.getElementById(
                    VIEWPORT_ID
                ),

            leftButton:
                document.getElementById(
                    LEFT_BUTTON_ID
                ),

            rightButton:
                document.getElementById(
                    RIGHT_BUTTON_ID
                )

        };

    }


    /*
    ============================================================
    BUTTON STATE
    ============================================================
    */

    function updateButtons() {

        const {
            viewport,
            leftButton,
            rightButton
        } = getElements();


        if (!viewport) {

            return;

        }


        const maximumScroll =
            Math.max(
                0,
                viewport.scrollWidth -
                viewport.clientWidth
            );


        const currentScroll =
            viewport.scrollLeft;


        if (leftButton) {

            leftButton.disabled =
                currentScroll <= 2;

        }


        if (rightButton) {

            rightButton.disabled =
                currentScroll >=
                maximumScroll - 2;

        }

    }


    /*
    ============================================================
    MOVEMENT AMOUNT
    ============================================================
    */

    function getMovementAmount() {

        const {
            viewport
        } = getElements();


        if (!viewport) {

            return 0;

        }


        return Math.max(
            viewport.clientWidth * 0.80,
            300
        );

    }


    /*
    ============================================================
    MOVE LEFT
    ============================================================
    */

    function moveLeft() {

        const {
            viewport
        } = getElements();


        if (!viewport) {

            return;

        }


        const amount =
            getMovementAmount();


        viewport.scrollBy({

            left: -amount,

            top: 0,

            behavior: "smooth"

        });


    }


    /*
    ============================================================
    MOVE RIGHT
    ============================================================
    */

    function moveRight() {

        const {
            viewport
        } = getElements();


        if (!viewport) {

            return;

        }


        const amount =
            getMovementAmount();


        viewport.scrollBy({

            left: amount,

            top: 0,

            behavior: "smooth"

        });


    }


    /*
    ============================================================
    EVENT BINDING
    ============================================================
    */

    function bindEvents() {

        const {
            viewport,
            leftButton,
            rightButton
        } = getElements();


        if (
            !viewport ||
            !leftButton ||
            !rightButton
        ) {

            return false;

        }


        if (
            viewport.dataset
                .geoshieldHorizontalNavBound ===
            "true"
        ) {

            return true;

        }


        viewport.dataset
            .geoshieldHorizontalNavBound =
            "true";


        leftButton.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                event.stopPropagation();

                moveLeft();

            }
        );


        rightButton.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                event.stopPropagation();

                moveRight();

            }
        );


        viewport.addEventListener(
            "scroll",
            function () {

                updateButtons();

            },
            {
                passive: true
            }
        );


        window.addEventListener(
            "resize",
            function () {

                updateButtons();

            },
            {
                passive: true
            }
        );


        return true;

    }


    /*
    ============================================================
    INITIALIZATION
    ============================================================
    */

    function initialize() {

        if (initialized) {

            updateButtons();

            return;

        }


        if (!bindEvents()) {

            window.setTimeout(
                initialize,
                250
            );

            return;

        }


        initialized = true;


        updateButtons();


        console.log(
            "GeoShield Satellite Horizontal Navigator: READY"
        );

    }


    /*
    ============================================================
    PUBLIC API
    ============================================================
    */

    window.GeoShieldSatelliteNavigator = {

        initialize:
            initialize,

        left:
            moveLeft,

        right:
            moveRight,

        refresh:
            updateButtons

    };


    /*
    ============================================================
    START
    ============================================================
    */

    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            initialize,
            {
                once: true
            }
        );

    }
    else {

        initialize();

    }


})();
