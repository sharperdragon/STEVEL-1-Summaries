function filterCards() {
  const input = document.getElementById("searchInput").value.toLowerCase();
  const cards = document.querySelectorAll(".summary-card");
  cards.forEach(card => {
    const text = card.textContent.toLowerCase();
    card.style.display = text.includes(input) ? "block" : "none";
  });
}

function enableTableSearch() {
  const input = document.getElementById("searchInput");
  if (!input) return;

  input.addEventListener("input", () => {
    const query = input.value.toLowerCase();
    document.querySelectorAll("td").forEach(cell => {
      const text = cell.textContent.toLowerCase();
      cell.style.opacity = text.includes(query) ? "" : "0.2";
    });
  });
}

function injectBuzzScrollCSS(duration) {
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

      const itemCount = items.length;
      const randomOffset = Math.floor(Math.random() * itemCount);
      const previewItems = items.slice(randomOffset).concat(items.slice(0, randomOffset));
      track.innerHTML = previewItems.join("      ");
      track.style.transform = `translateX(-${(randomOffset / itemCount) * 100}%)`;

      requestAnimationFrame(() => {
        const fullWidth = track.scrollWidth;
        const speedPxPerSec = 38;
        const duration = Math.max(20, Math.round(fullWidth / speedPxPerSec));
        injectBuzzScrollCSS(duration);
      });
    })
    .catch(err => {
      console.error("❌ Failed to load buzzwords:", err);
      track.textContent = "Buzzwords unavailable.";
    });
}

function setupRapidReviewCarousel() {
  const container = document.getElementById("rapidReviewCarousel");
  if (!container) return;
  // Placeholder: future implementation
  container.innerHTML = "<p style='color:#777;'>Rapid Review Carousel coming soon.</p>";
}

function initSearchBinding() {
  const searchInput = document.getElementById("searchInput");
  if (!searchInput) return;

  if (document.querySelector(".summary-card")) {
    searchInput.addEventListener("input", filterCards);
  } else if (document.querySelector("td")) {
    enableTableSearch();
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadBuzzwords();
  setupRapidReviewCarousel();
  initSearchBinding();
});