document.addEventListener("DOMContentLoaded", () => {
    createModal();
    loadDashboard();
    loadSuggestions();

    document.getElementById("searchButton")
        .addEventListener("click", searchPlanet);
});

/* ===============================
   CATEGORY SAFE CLASS
================================= */

function getBadgeClass(category) {
    if (!category) return "badge-unknown";
    return "badge-" + category.toLowerCase().replace(/\s+/g, "-");
}

/* ===============================
   DASHBOARD
================================= */

async function loadDashboard() {
    try {
        const res = await fetch('/dashboard');
        const data = await res.json();

        const summary = data.summary;
        const hazardous = data.hazardous_asteroids_today;

        document.getElementById("summaryCard").innerHTML = `
            <h3>Planet Statistics</h3>
            <p>Total Planets: ${summary.total_planets}</p>
            <p>Average Radius: ${summary.average_radius ?? "?"} Earth</p>
            <p>Latest Discovery: ${summary.latest_discovery_year}</p>
            <p>Common Method: ${summary.most_common_discovery_method}</p>
        `;

        document.getElementById("categoryCard").innerHTML = `
            <h3>Category Distribution</h3>
            ${Object.entries(summary.category_distribution)
                .map(([k,v]) => `<p>${k}: ${v}</p>`).join("")}
        `;

        document.getElementById("asteroidCard").innerHTML = `
            <h3>Hazardous Asteroids Today</h3>
            ${hazardous.length === 0
                ? "<p>No hazardous objects detected.</p>"
                : hazardous.map(a => `<p>${a.name}</p>`).join("")}
        `;

    } catch (err) {
        console.error("Dashboard error:", err);
    }
}

/* ===============================
   SUGGESTIONS
================================= */

async function loadSuggestions() {
    try {
        const res = await fetch('/suggestions');
        const data = await res.json();
        renderCards(data, "suggestions");
    } catch (err) {
        console.error("Suggestion error:", err);
    }
}

/* ===============================
   SEARCH
================================= */

async function searchPlanet() {
    const query = document.getElementById("searchInput").value.trim();
    if (!query) return;

    try {
        const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
        const data = await res.json();
        renderCards(data, "results");
    } catch (err) {
        console.error("Search error:", err);
    }
}

/* ===============================
   RENDER CARDS
================================= */

function renderCards(planets, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    if (!Array.isArray(planets) || planets.length === 0) {
        container.innerHTML = "<p>No data available.</p>";
        return;
    }

    planets.forEach(p => {
        const badgeClass = getBadgeClass(p.classification);

        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
            <h3>${p.name}</h3>
            <p>Star: ${p.host_star}</p>
            <p>Radius: ${p.radius_earth ?? "?"} Earth</p>
            <span class="badge ${badgeClass}">
                ${p.classification}
            </span>
        `;

        card.onclick = () => openModal(p);
        container.appendChild(card);
    });
}

/* ===============================
   MODAL
================================= */

function createModal() {
    const modal = document.createElement("div");
    modal.id = "planetModal";
    modal.innerHTML = `
        <div class="modal-content">
            <span id="closeModal">&times;</span>
            <div id="modalBody"></div>
        </div>
    `;
    document.body.appendChild(modal);

    document.getElementById("closeModal").onclick = closeModal;

    modal.onclick = (e) => {
        if (e.target === modal) closeModal();
    };
}

function openModal(p) {
    document.getElementById("modalBody").innerHTML = `
        <h2>${p.name}</h2>
        <p>Host Star: ${p.host_star}</p>
        <p>Radius: ${p.radius_earth ?? "?"} Earth</p>
        <p>Mass: ${p.mass_earth ?? "?"} Earth</p>
        <p>Classification: ${p.classification}</p>
    `;
    document.getElementById("planetModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("planetModal").style.display = "none";
}
