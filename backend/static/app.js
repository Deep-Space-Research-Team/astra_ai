async function loadSuggestions() {
    const res = await fetch('/suggestions');
    const data = await res.json();
    display(data, "suggestions");
}

async function searchPlanet() {
    const query = document.getElementById("searchInput").value;
    if (!query) return;

    const res = await fetch(`/search?q=${query}`);
    const data = await res.json();
    display(data, "results");
}

function display(planets, elementId) {
    const container = document.getElementById(elementId);
    container.innerHTML = "";

    planets.forEach(p => {
        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
            <h3>${p.name}</h3>
            <p><strong>Star:</strong> ${p.host_star || "Unknown"}</p>
            <p><strong>Radius:</strong> ${p.radius_earth || "?"} Earth</p>
            <span class="badge">${p.classification || "Unknown"}</span>
        `;

        container.appendChild(card);
    });
}

loadSuggestions();
