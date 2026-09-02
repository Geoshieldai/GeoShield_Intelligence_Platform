(function () {
    "use strict";

    const MAP_PAGE = "geoshieldMapPage";
    const INTELLIGENCE_PAGE = "geoshieldIntelligencePage";

    let currentWorkspace = "map";

    function setWorkspace(mode) {
        const mapPage = document.getElementById(MAP_PAGE);
        const intelligencePage = document.getElementById(INTELLIGENCE_PAGE);

        if (!mapPage || !intelligencePage) {
            console.error("GeoShield workspace pages not found.");
            return;
        }

        currentWorkspace =
            mode === "intelligence" ? "intelligence" : "map";

        mapPage.classList.toggle(
            "workspace-page-active",
            currentWorkspace === "map"
        );

        intelligencePage.classList.toggle(
            "workspace-page-active",
            currentWorkspace === "intelligence"
        );

        document.body.classList.toggle(
            "geoshield-map-mode",
            currentWorkspace === "map"
        );

        document.body.classList.toggle(
            "geoshield-intelligence-mode",
            currentWorkspace === "intelligence"
        );

        updateNavigator();

        console.log(
            "GeoShield workspace:",
            currentWorkspace.toUpperCase()
        );
    }

    function goToMap() {
        setWorkspace("map");
    }

    function goToIntelligence() {
        setWorkspace("intelligence");
    }

    function updateNavigator() {
        const mapButton =
            document.getElementById("workspaceMapArrow");

        const intelligenceButton =
            document.getElementById(
                "workspaceIntelligenceArrow"
            );

        if (!mapButton || !intelligenceButton) {
            return;
        }

        const isMap = currentWorkspace === "map";

        mapButton.disabled = isMap;
        intelligenceButton.disabled = !isMap;

        mapButton.classList.toggle("active", isMap);
        intelligenceButton.classList.toggle("active", !isMap);
    }

    function createNavigator() {
        let nav =
            document.getElementById("workspaceNavigator");

        if (!nav) {
            nav = document.createElement("div");

            nav.id = "workspaceNavigator";
            nav.className = "workspace-navigator";

            nav.innerHTML = `
                <button
                    type="button"
                    id="workspaceMapArrow"
                    class="workspace-nav-arrow"
                    aria-label="Main Map"
                    title="Main Map">
                    ←
                </button>

                <div
                    class="workspace-nav-divider"
                    aria-hidden="true">
                </div>

                <button
                    type="button"
                    id="workspaceIntelligenceArrow"
                    class="workspace-nav-arrow"
                    aria-label="Satellite Intelligence"
                    title="Satellite Intelligence">
                    →
                </button>
            `;

            document.body.appendChild(nav);
        }

        if (nav.dataset.bound !== "true") {
            nav.addEventListener("click", function (event) {
                const button =
                    event.target.closest("button");

                if (!button) {
                    return;
                }

                if (
                    button.id ===
                    "workspaceMapArrow"
                ) {
                    goToMap();
                    return;
                }

                if (
                    button.id ===
                    "workspaceIntelligenceArrow"
                ) {
                    goToIntelligence();
                }
            });

            nav.dataset.bound = "true";
        }

        updateNavigator();
    }

    function initialize() {
        createNavigator();
        setWorkspace("map");

        console.log(
            "GeoShield Workspace Navigation READY"
        );
    }

    window.GeoShieldWorkspace = {
        initialize: initialize,
        goToMap: goToMap,
        goToIntelligence: goToIntelligence,
        getCurrentWorkspace: function () {
            return currentWorkspace;
        }
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
