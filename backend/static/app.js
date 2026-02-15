function display(planets) {
    let html = "";

    if (!planets || planets.length === 0) {
        html = "<p>No results found.</p>";
    } else {
        planets.forEach(p => {
            html += `
                <div class="card">
                    <h3>${p.name}</h3>
                    <p>Habitability Score: ${p.habitability_score}</p>
                    <button onclick="viewObject('${p.name}')">
                        View Details
                    </button>
                </div>
            `;
        });
    }

    document.getElementById("results").innerHTML = html;
}

function searchPlanet() {
    const query = document.getElementById("searchBox").value;
    if (!query) return;

    fetch(`/astra/search?q=${query}`)
    .then(res => res.json())
    .then(data => display(data));
}

function loadTop() {
    fetch(`/astra/exoplanets?limit=10`)
    .then(res => res.json())
    .then(data => display(data));
}

function viewObject(name) {
    window.location.href = `/static/object.html?name=${encodeURIComponent(name)}`;
}
