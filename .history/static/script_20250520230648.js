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
                ? data.map(item => `<span class="buzzword"><strong>${item.term}</strong><span class="assoc"> — ${item.assoc}</span></span>`)
                : Object.entries(data).map(([term, assoc]) => `<span class="buzzword"><strong>${term}</strong><span class="assoc"> — ${assoc}</span></span>`);

            track.innerHTML = items.join("      ");
            // Adjust scroll speed based on number of terms and viewport width
            const numTerms = items.length;
            const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
            const duration = Math.max(20, Math.round((numTerms  vw) / 1000)); // e.g. 1s per 1000px*term
            track.style.animationDuration = `${duration}s`;
        })
        .catch(err => {
            console.error("❌ Failed to load buzzwords:", err);
            track.textContent = "Buzzwords unavailable.";
        });
}

document.addEventListener("DOMContentLoaded", () => {
    loadBuzzwords();
});