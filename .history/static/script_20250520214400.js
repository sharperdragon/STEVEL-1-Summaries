function filterCards() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const cards = document.querySelectorAll(".summary-card");

    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(input) ? "block" : "none";
    });
}

function loadBuzzwords() {
    const track = document.querySelector(".buzz-track");
    if (!track) return;

    fetch("/STEVEL-1-Summaries/utils/Texts/buzzwords.json")
        .then(response => response.json())
        .then(data => {
            const items = Array.isArray(data)
                ? data.map(item => `<span class="buzzword" title="${item.assoc}">${item.term}</span>`)
                : Object.entries(data).map(([term, assoc]) => `<span class="buzzword" title="${assoc}">${term}</span>`);

            track.innerHTML = items.join("  ");
        })
        .catch(err => {
            console.error("❌ Failed to load buzzwords:", err);
            track.textContent = "Buzzwords unavailable.";
        });
}

document.addEventListener("DOMContentLoaded", () => {
    loadBuzzwords();
});