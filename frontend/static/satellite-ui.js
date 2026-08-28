/*
============================================================
 GeoShield AI Enterprise
 Satellite Intelligence Hub UI
============================================================
*/

window.SatelliteUI = {

    containerId: "satelliteHub",


    initialize() {

        this.container =
            document.getElementById(this.containerId);

        if (!this.container) {

            console.warn(
                "Satellite Hub container not found."
            );

            return;
        }

        this.load();
    },


    async load() {

        this.setLoading();

        try {

            const data =
                await window.SatelliteAPI.getSatellites();

            this.render(data.satellites || []);

        }
        catch (error) {

            console.error(
                "Satellite Hub failed:",
                error
            );

            this.setError(error);
        }
    },


    setLoading() {

        this.container.innerHTML = `
            <div class="satellite-loading">
                Loading satellite intelligence systems...
            </div>
        `;
    },


    setError(error) {

        this.container.innerHTML = `
            <div class="satellite-error">

                <strong>
                    Satellite Intelligence API Error
                </strong>

                <span>
                    ${this.escape(error.message)}
                </span>

            </div>
        `;
    },


    render(satellites) {

        if (!satellites.length) {

            this.container.innerHTML = `
                <div class="satellite-empty">
                    No satellite systems registered.
                </div>
            `;

            return;
        }

        this.container.innerHTML = `

            <div class="satellite-grid">

                ${satellites
                    .map(
                        satellite =>
                            this.createCard(satellite)
                    )
                    .join("")
                }

            </div>

        `;
    },


    createCard(satellite) {

        const statusClass =
            satellite.status === "online"
                ? "online"
                : satellite.status === "integrating"
                    ? "integrating"
                    : "offline";

        const statusLabel =
            satellite.status === "online"
                ? "ONLINE"
                : satellite.status === "integrating"
                    ? "INTEGRATING"
                    : "OFFLINE";

        const capabilities =
            (satellite.capabilities || [])
                .slice(0, 5)
                .map(
                    capability =>
                        `<span>${this.escape(capability)}</span>`
                )
                .join("");

        return `

            <article
                class="satellite-card"
                data-satellite-id="${this.escape(satellite.id)}"
            >

                <div class="satellite-card-header">

                    <div>

                        <h3>
                            ?? ${this.escape(satellite.name)}
                        </h3>

                        <p>
                            ${this.escape(satellite.provider)}
                        </p>

                    </div>

                    <span
                        class="satellite-status ${statusClass}"
                    >
                        ${statusLabel}
                    </span>

                </div>


                <div class="satellite-category">

                    ${this.escape(satellite.category)}

                </div>


                <p class="satellite-description">

                    ${this.escape(satellite.description)}

                </p>


                <div class="satellite-capabilities">

                    ${capabilities}

                </div>


                <div class="satellite-card-actions">

                    <button
                        type="button"
                        onclick="SatelliteUI.open('${this.escape(satellite.id)}')"
                    >
                        OPEN
                    </button>

                    <button
                        type="button"
                        onclick="SatelliteUI.diagnostics('${this.escape(satellite.id)}')"
                    >
                        DIAGNOSTICS
                    </button>

                </div>

            </article>

        `;
    },


    async open(id) {

        try {

            const data =
                await window.SatelliteAPI.getSatellite(id);

            console.log(
                "Satellite selected:",
                data
            );

            const card =
                document.querySelector(
                    `[data-satellite-id="${id}"]`
                );

            if (card) {

                card.classList.toggle(
                    "satellite-selected"
                );
            }

        }
        catch (error) {

            console.error(
                "Unable to open satellite:",
                error
            );
        }
    },


    async diagnostics(id) {

        try {

            const [status, capabilities] =
                await Promise.all([
                    window.SatelliteAPI.getStatus(id),
                    window.SatelliteAPI.getCapabilities(id)
                ]);

            console.log(
                "Satellite diagnostics:",
                {
                    status,
                    capabilities
                }
            );

            alert(
                `${status.name}\n\n` +
                `Provider: ${status.provider}\n` +
                `Status: ${status.connection_status}\n\n` +
                `Capabilities:\n` +
                capabilities.capabilities.join("\n")
            );

        }
        catch (error) {

            console.error(
                "Satellite diagnostics failed:",
                error
            );
        }
    },


    escape(value) {

        return String(value ?? "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

};


document.addEventListener(
    "DOMContentLoaded",
    () => SatelliteUI.initialize()
);
