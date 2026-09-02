/*
============================================================
 GeoShield AI Enterprise
 Satellite Intelligence API
============================================================
*/

window.SatelliteAPI = {

    async getSatellites() {

        const response = await fetch("/satellites");

        if (!response.ok) {
            throw new Error(
                `Satellite API returned ${response.status}`
            );
        }

        return await response.json();
    },


    async getSatellite(id) {

        const response = await fetch(
            `/satellites/${encodeURIComponent(id)}`
        );

        if (!response.ok) {
            throw new Error(
                `Satellite API returned ${response.status}`
            );
        }

        return await response.json();
    },


    async getStatus(id) {

        const response = await fetch(
            `/satellites/${encodeURIComponent(id)}/status`
        );

        if (!response.ok) {
            throw new Error(
                `Satellite status returned ${response.status}`
            );
        }

        return await response.json();
    },


    async getCapabilities(id) {

        const response = await fetch(
            `/satellites/${encodeURIComponent(id)}/capabilities`
        );

        if (!response.ok) {
            throw new Error(
                `Satellite capabilities returned ${response.status}`
            );
        }

        return await response.json();
    }

};
