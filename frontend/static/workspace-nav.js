(function () {

    "use strict";

    /*
    ============================================================
    GeoShield AI Enterprise
    Workspace Navigation Controller
    ============================================================

    ARCHITECTURE

        MAIN MAP
            |
            | explicit button action
            v
        SATELLITE INTELLIGENCE

    RULES

    1. No viewport movement
    2. No automatic viewport detection
    3. No anchor navigation
    4. No smooth transitions between workspaces
    5. No automatic workspace detection
    6. Workspace state is controlled only by BODY classes
    7. Navigator is created directly under BODY
    8. Only one navigator may exist

    ============================================================
    */

    const MAP_MODE =
        "geoshield-map-mode";

    const INTELLIGENCE_MODE =
        "geoshield-intelligence-mode";

    let currentWorkspace =
        "map";


    /*
    ============================================================
    WORKSPACE STATE
    ============================================================
    */

    function setWorkspace(mode) {

        currentWorkspace =
            mode === "intelligence"
                ? "intelligence"
                : "map";


        document.body.classList.remove(
            MAP_MODE,
            INTELLIGENCE_MODE
        );


        document.body.classList.add(
            currentWorkspace === "intelligence"
                ? INTELLIGENCE_MODE
                : MAP_MODE
        );


        /*
        --------------------------------------------------------
        No viewport manipulation occurs here.

        The CSS workspace state determines which interface
        is visible.
        --------------------------------------------------------
        */

        updateNavigator();


        console.log(
            "GeoShield workspace:",
            currentWorkspace.toUpperCase()
        );

    }


    /*
    ============================================================
    PUBLIC WORKSPACE ACTIONS
    ============================================================
    */

    function goToMainMap() {

        setWorkspace(
            "map"
        );

    }


    function goToIntelligence() {

        setWorkspace(
            "intelligence"
        );

    }


    /*
    ============================================================
    NAVIGATOR STATE
    ============================================================
    */

    function updateNavigator() {

        const mapArrow =
            document.getElementById(
                "workspaceMapArrow"
            );

        const intelligenceArrow =
            document.getElementById(
                "workspaceIntelligenceArrow"
            );


        if (
            !mapArrow ||
            !intelligenceArrow
        ) {

            return;

        }


        const isMap =
            currentWorkspace === "map";

        const isIntelligence =
            currentWorkspace === "intelligence";


        mapArrow.disabled =
            isMap;

        intelligenceArrow.disabled =
            isIntelligence;


        mapArrow.classList.toggle(
            "active",
            isMap
        );

        intelligenceArrow.classList.toggle(
            "active",
            isIntelligence
        );


        mapArrow.setAttribute(
            "aria-current",
            isMap
                ? "page"
                : "false"
        );

        intelligenceArrow.setAttribute(
            "aria-current",
            isIntelligence
                ? "page"
                : "false"
        );

    }


    /*
    ============================================================
    CREATE WORKSPACE NAVIGATOR
    ============================================================
    */

    function createWorkspaceNavigator() {

        let navigator =
            document.getElementById(
                "workspaceNavigator"
            );


        if (navigator) {

            bindNavigationEvents(
                navigator
            );

            updateNavigator();

            return;

        }


        navigator =
            document.createElement(
                "div"
            );


        navigator.id =
            "workspaceNavigator";


        navigator.className =
            "workspace-navigator";


        navigator.setAttribute(
            "aria-label",
            "GeoShield workspace navigation"
        );


        navigator.innerHTML = `

            <button
                type="button"
                class="workspace-nav-arrow"
                id="workspaceMapArrow"
                title="Main Map"
                aria-label="Go to Main Map">

                ↑

            </button>


            <div
                class="workspace-nav-divider"
                aria-hidden="true">
            </div>


            <button
                type="button"
                class="workspace-nav-arrow"
                id="workspaceIntelligenceArrow"
                title="Satellite Intelligence"
                aria-label="Go to Satellite Intelligence">

                ↓

            </button>

        `;


        /*
        --------------------------------------------------------
        The navigator is attached directly to BODY.

        It is never inserted into any workspace container.
        --------------------------------------------------------
        */

        document.body.appendChild(
            navigator
        );


        bindNavigationEvents(
            navigator
        );


        updateNavigator();

    }


    /*
    ============================================================
    NAVIGATION EVENTS
    ============================================================
    */

    function bindNavigationEvents(
        navigator
    ) {

        if (
            navigator.dataset
                .geoshieldBound === "true"
        ) {

            return;

        }


        navigator.dataset
            .geoshieldBound =
            "true";


        navigator.addEventListener(
            "click",
            function (event) {

                const button =
                    event.target.closest(
                        "button"
                    );


                if (!button) {

                    return;

                }


                if (
                    button.id ===
                    "workspaceMapArrow"
                ) {

                    goToMainMap();

                    return;

                }


                if (
                    button.id ===
                    "workspaceIntelligenceArrow"
                ) {

                    goToIntelligence();

                    return;

                }

            }
        );

    }


    /*
    ============================================================
    INITIALIZATION
    ============================================================
    */

    function initialize() {

        createWorkspaceNavigator();


        /*
        --------------------------------------------------------
        Always begin in Main Map mode.
        --------------------------------------------------------
        */

        setWorkspace(
            "map"
        );


        console.log(
            "======================================"
        );

        console.log(
            "GeoShield Workspace Navigation"
        );

        console.log(
            "Mode: STATIC / DETERMINISTIC"
        );

        console.log(
            "Main Map: ISOLATED"
        );

        console.log(
            "Satellite Intelligence: ISOLATED"
        );

        console.log(
            "Automatic viewport control: OFF"
        );

        console.log(
            "Automatic workspace detection: OFF"
        );

        console.log(
            "Anchor navigation: OFF"
        );

        console.log(
            "Navigator duplication: BLOCKED"
        );

        console.log(
            "======================================"
        );

    }


    /*
    ============================================================
    PUBLIC API
    ============================================================
    */

    window.GeoShieldWorkspace = {

        initialize:
            initialize,

        goToMap:
            goToMainMap,

        goToIntelligence:
            goToIntelligence,

        getCurrentWorkspace:
            function () {

                return currentWorkspace;

            }

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
