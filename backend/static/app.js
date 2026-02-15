async function load() {
    const res = await fetch('/astra/exoplanets?limit=10');
    const data = await res.json();

    let html = "";
    data.forEach(p => {
        html += `<h3>${p.name}</h3>
                 <p>Score: ${p.habitability_score}</p>
                 <hr/>`;
    });

    document.getElementById("results").innerHTML = html;
}
