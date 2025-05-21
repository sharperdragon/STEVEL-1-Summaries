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

            // Randomize start position by shifting the container
            const itemCount = items.length;
            const randomOffset = Math.floor(Math.random() * itemCount);
            const previewItems = items.slice(randomOffset).concat(items.slice(0, randomOffset));
            track.innerHTML = previewItems.join("      ");
            track.style.transform = `translateX(-${(randomOffset / itemCount) * 100}%)`;
            // Adjust scroll speed based on total pixel width of all items
            requestAnimationFrame(() => {
              const fullWidth = track.scrollWidth;
              const speedPxPerSec = 30; // adjust this value to fine-tune perceived speed
              const duration = Math.max(20, Math.round(fullWidth / speedPxPerSec));
              // Inject smooth scroll CSS with pause on hover
              const style = document.createElement("style");
              style.innerHTML = `
                .buzz-track {
                  --scroll-duration: ${duration}s;
                  animation: scroll-buzz var(--scroll-duration) ease-out infinite;
                }
                .buzz-track:hover {
                  animation-play-state: paused;
                }
                @keyframes scroll-buzz {
                  0% { transform: translateX(0); }
                  100% { transform: translateX(-100%); }
                }
              `;
              document.head.appendChild(style);
            });
        })
        .catch(err => {
            console.error("❌ Failed to load buzzwords:", err);
            track.textContent = "Buzzwords unavailable.";
        });
}

document.addEventListener("DOMContentLoaded", () => {
    loadBuzzwords();
});