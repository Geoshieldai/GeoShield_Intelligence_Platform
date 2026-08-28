/*
==============================================================
GeoShield AI Enterprise
Sentinel-2 Product UI Controller
==============================================================
*/

window.GeoShield = window.GeoShield || {};

window.GeoShield.sentinel2UI = {

    containerId: "sentinel2Product",

    /*
    ----------------------------------------------------------
    Initialize
    ----------------------------------------------------------
    */

    initialize: function () {

        const container =
            document.getElementById(
                this.containerId
            );

        if (!container) {

            console.warn(
                "Sentinel-2 product container not found."
            );

            return false;

        }

        this.container = container;

        this.bindEvents();

        this.showEmptyState();

        console.log(
            "Sentinel-2 UI initialized"
        );

        return true;

    },

    /*
    ----------------------------------------------------------
    Bind UI events
    ----------------------------------------------------------
    */

    bindEvents: function () {

        const searchButton =
            document.getElementById(
                "sentinel2SearchBtn"
            );

        if (searchButton) {

            searchButton.addEventListener(
                "click",
                () => {

                    this.searchScenes();

                }
            );

        }

    },

    /*
    ----------------------------------------------------------
    Search
    ----------------------------------------------------------
    */

    async searchScenes() {

        this.setStatus(
            "Searching Sentinel-2 catalogue..."
        );

        try {

            const county =
                window.GeoShield?.state
                    ?.currentCounty || null;

            const result =
                await window.GeoShield
                    .sentinel2API
                    .search({
                        county: county,
                        maxCloud: 30
                    });

            const scenes =
                result?.scenes ||
                result?.results ||
                [];

            window.GeoShield
                .sentinel2
                .setScenes(scenes);

            this.renderScenes(scenes);

            this.setStatus(
                `${scenes.length} scene(s) found`
            );

        }
        catch (error) {

            console.error(
                "Sentinel-2 search failed:",
                error
            );

            this.showError(
                error.message
            );

        }

    },

    /*
    ----------------------------------------------------------
    Render scenes
    ----------------------------------------------------------
    */

    renderScenes: function (scenes) {

        const list =
            document.getElementById(
                "sentinel2SceneList"
            );

        if (!list) {
            return;
        }

        if (!Array.isArray(scenes) ||
            scenes.length === 0) {

            list.innerHTML = `
                <div class="sentinel2-empty">
                    No Sentinel-2 scenes available.
                </div>
            `;

            return;

        }

        list.innerHTML =
            scenes
                .map(scene =>
                    window.GeoShield
                        .sentinel2
                        .renderSceneCard(scene)
                )
                .join("");

        this.bindSceneSelection();

    },

    /*
    ----------------------------------------------------------
    Scene selection
    ----------------------------------------------------------
    */

    bindSceneSelection: function () {

        const buttons =
            document.querySelectorAll(
                "[data-select-scene]"
            );

        buttons.forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    const id =
                        button.dataset.selectScene;

                    this.selectScene(id);

                }
            );

        });

    },

    /*
    ----------------------------------------------------------
    Select scene
    ----------------------------------------------------------
    */

    selectScene: function (sceneId) {

        const scenes =
            window.GeoShield
                .sentinel2
                .state
                .scenes;

        const scene =
            scenes.find(
                item =>
                    item.id === sceneId
            );

        if (!scene) {

            this.showError(
                "Selected Sentinel-2 scene was not found."
            );

            return;

        }

        window.GeoShield
            .sentinel2
            .selectScene(scene);

        this.showSelectedScene(scene);

        console.log(
            "Selected Sentinel-2 scene:",
            scene
        );

    },

    /*
    ----------------------------------------------------------
    Selected scene display
    ----------------------------------------------------------
    */

    showSelectedScene: function (scene) {

        const selected =
            document.getElementById(
                "sentinel2SelectedScene"
            );

        if (!selected) {
            return;
        }

        selected.innerHTML = `

            <div class="sentinel2-selected">

                <div>
                    <span class="label">
                        Selected Scene
                    </span>

                    <strong>
                        ${window.GeoShield
                            .sentinel2
                            .escapeHtml(
                                scene.productId
                            )}
                    </strong>
                </div>

                <div>
                    <span class="label">
                        Acquisition
                    </span>

                    <span>
                        ${window.GeoShield
                            .sentinel2
                            .escapeHtml(
                                window.GeoShield
                                    .sentinel2
                                    .formatDate(
                                        scene.acquisitionDate
                                    )
                            )}
                    </span>
                </div>

                <div>
                    <span class="label">
                        Cloud Cover
                    </span>

                    <span>
                        ${scene.cloudCover.toFixed(1)}%
                    </span>
                </div>

            </div>

        `;

    },

    /*
    ----------------------------------------------------------
    Empty state
    ----------------------------------------------------------
    */

    showEmptyState: function () {

        const list =
            document.getElementById(
                "sentinel2SceneList"
            );

        if (!list) {
            return;
        }

        list.innerHTML = `
            <div class="sentinel2-empty">
                Select a county or search for
                available Sentinel-2 imagery.
            </div>
        `;

    },

    /*
    ----------------------------------------------------------
    Status
    ----------------------------------------------------------
    */

    setStatus: function (message) {

        const status =
            document.getElementById(
                "sentinel2Status"
            );

        if (status) {
            status.textContent = message;
        }

    },

    /*
    ----------------------------------------------------------
    Error
    ----------------------------------------------------------
    */

    showError: function (message) {

        this.setStatus(
            "Sentinel-2 error: " + message
        );

        const list =
            document.getElementById(
                "sentinel2SceneList"
            );

        if (list) {

            list.innerHTML = `
                <div class="sentinel2-error">
                    ${window.GeoShield
                        .sentinel2
                        .escapeHtml(message)}
                </div>
            `;

        }

    }

};
