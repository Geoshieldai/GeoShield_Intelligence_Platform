/*
==============================================================
GeoShield AI Enterprise
Sentinel-2 API Client
==============================================================
*/

window.GeoShield = window.GeoShield || {};

window.GeoShield.sentinel2API = {

    baseURL: "/sentinel2",

    /*
    ----------------------------------------------------------
    Generic request helper
    ----------------------------------------------------------
    */

    request: async function (endpoint, options = {}) {

        const response = await fetch(
            this.baseURL + endpoint,
            {
                method: options.method || "GET",

                headers: {
                    "Accept": "application/json",

                    ...(options.body
                        ? {
                            "Content-Type":
                                "application/json"
                        }
                        : {})
                },

                body: options.body
                    ? JSON.stringify(options.body)
                    : undefined
            }
        );

        let data = null;

        try {
            data = await response.json();
        }
        catch (error) {

            throw new Error(
                "Sentinel-2 server returned invalid JSON."
            );

        }

        if (!response.ok) {

            const message =
                data?.detail ||
                data?.message ||
                data?.error ||
                `HTTP ${response.status}`;

            throw new Error(message);

        }

        return data;

    },

    /*
    ----------------------------------------------------------
    Health
    ----------------------------------------------------------
    */

    health: async function () {

        return await this.request("/health");

    },

    /*
    ----------------------------------------------------------
    Search Sentinel-2 scenes
    ----------------------------------------------------------
    */

    search: async function (params = {}) {

        const query =
            new URLSearchParams();

        if (params.county) {
            query.set(
                "county",
                params.county
            );
        }

        if (params.latitude !== undefined) {
            query.set(
                "latitude",
                params.latitude
            );
        }

        if (params.longitude !== undefined) {
            query.set(
                "longitude",
                params.longitude
            );
        }

        if (params.startDate) {
            query.set(
                "start_date",
                params.startDate
            );
        }

        if (params.endDate) {
            query.set(
                "end_date",
                params.endDate
            );
        }

        if (params.maxCloud !== undefined) {
            query.set(
                "max_cloud",
                params.maxCloud
            );
        }

        const suffix =
            query.toString()
                ? "?" + query.toString()
                : "";

        return await this.request(
            "/search" + suffix
        );

    },

    /*
    ----------------------------------------------------------
    Scene details
    ----------------------------------------------------------
    */

    getScene: async function (sceneId) {

        if (!sceneId) {
            throw new Error(
                "Scene ID is required."
            );
        }

        return await this.request(
            "/scene/" +
            encodeURIComponent(sceneId)
        );

    },

    /*
    ----------------------------------------------------------
    Preview
    ----------------------------------------------------------
    */

    getPreviewURL: function (sceneId) {

        if (!sceneId) {
            return null;
        }

        return (
            this.baseURL +
            "/preview/" +
            encodeURIComponent(sceneId)
        );

    },

    /*
    ----------------------------------------------------------
    Imagery layer URL
    ----------------------------------------------------------
    */

    getImageryURL: function (
        sceneId,
        options = {}
    ) {

        if (!sceneId) {
            return null;
        }

        const query =
            new URLSearchParams();

        if (options.band) {
            query.set(
                "band",
                options.band
            );
        }

        if (options.index) {
            query.set(
                "index",
                options.index
            );
        }

        const suffix =
            query.toString()
                ? "?" + query.toString()
                : "";

        return (
            this.baseURL +
            "/imagery/" +
            encodeURIComponent(sceneId) +
            suffix
        );

    },

    /*
    ----------------------------------------------------------
    NDVI endpoint
    ----------------------------------------------------------
    */

    getNDVIURL: function (sceneId) {

        if (!sceneId) {
            return null;
        }

        return (
            this.baseURL +
            "/ndvi/" +
            encodeURIComponent(sceneId)
        );

    }

};
