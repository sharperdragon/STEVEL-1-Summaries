/*** ─── BUZZWORDS ───────────────────────────────────────────── **/
function injectBuzzScrollCSS(duration) {
  const style = document.createElement("style");
  style.innerHTML = `
    .buzz-track {
      --scroll-duration: ${duration}s;
      animation: scroll-buzz var(--scroll-duration) linear infinite;
      will-change: transform;
    }
    .buzz-track.paused {
      animation-play-state: paused;
      transform: translateY(1px);
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

  fetch("/STEVEL-1-Summaries/static/data/buzzwords.json")
    .then(response => response.json())
    .then(data => {
      const items = Array.isArray(data)
        ? data.map(item => `<span class="buzzword"><strong>${item.term}</strong><span class="assoc"> — ${item.assoc}</span></span>`)
        : Object.entries(data).map(([term, assoc]) => `<span class="buzzword"><strong>${term}</strong><span class="assoc"> — ${assoc}</span></span>`);

      const itemCount = items.length;
      const randomOffset = Math.floor(Math.random() * itemCount);
      const previewItems = items.slice(randomOffset).concat(items.slice(0, randomOffset));
      track.innerHTML = previewItems.join("    ");
      // Ensure the buzz-track is wide enough to trigger scrolling
      track.style.minWidth = `${previewItems.length * 240}px`;
      // remove inline transform so CSS animation works
      track.style.removeProperty("transform");

      // Add hover event listeners to toggle .paused class for smooth transition
      track.addEventListener("mouseenter", () => {
        track.classList.add("paused");
      });
      track.addEventListener("mouseleave", () => {
        track.classList.remove("paused");
      });

      requestAnimationFrame(() => {
        const fullWidth = track.scrollWidth;
        const speedPxPerSec = 60;
        const duration = Math.max(20, Math.round(fullWidth / speedPxPerSec));
        injectBuzzScrollCSS(duration);
      });
    })
    .catch(err => {
      console.error("❌ Failed to load buzzwords:", err);
      track.textContent = "Buzzwords unavailable.";
    });
}

/*** ─── RAPID REVIEW CARDS ─────────────────────────────────── **/
function loadRapidReviewCards() {
  const container = document.getElementById("RapidCarousel");
  if (!container) return;

  fetch("/STEVEL-1-Summaries/static/data/rapid_cards.json")
    .then(res => res.json())
    .then(data => {
      const items = data.map(entry => `
        <div class="carousel-item">
          <div class="question">${entry.question}</div>
          <div class="answer">${entry.answer}</div>
        </div>
      `).join("");
      container.innerHTML = items;
      container.querySelectorAll(".answer").forEach(a => a.style.opacity = "0");
      setupRapidCarousel(); // initialize carousel only after loading
    })
    .catch(err => {
      console.error("❌ Failed to load rapid review cards:", err);
      container.innerHTML = "<p style='color:#777;'>Rapid Review unavailable.</p>";
    });
}

function setupRapidCarousel() {
  const container = document.getElementById("RapidCarousel");
  if (!container) return;

  const items = container.querySelectorAll(".carousel-item");
  if (items.length === 0) {
    container.innerHTML = "<p style='color:#777;'>Rapid Review Carousel coming soon.</p>";
    return;
  }

  let index = 0;

  const rotate = () => {
    items.forEach((item, i) => {
      item.style.display = i === index ? "block" : "none";
    });

    index = (index + 1) % items.length;
  };

  rotate();

  // Automatically show answer after 8 seconds if not hovered
  let answerShown = false;
  const currentItem = items[index];
  const answerDiv = currentItem.querySelector(".answer");

  if (answerDiv) {
    currentItem.addEventListener("mouseenter", () => {
      answerShown = true;
      answerDiv.style.opacity = "1";
    });

    currentItem.addEventListener("mouseleave", () => {
      answerShown = false;
    });

    setTimeout(() => {
      if (!answerShown) {
        answerDiv.style.opacity = "1";
      }
    }, 8000);
  }

  setInterval(rotate, 9600); // Rotate every 9 seconds
}

function resizeCarouselFont() {
  const container = document.getElementById("RapidCarousel");
  if (!container) return;

  const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
  const baseSize = Math.max(12, Math.min(22, vw * 0.018)); // clamp between 14px–18px
  container.style.fontSize = `${baseSize}px`;
}

/*** ─── SEARCH FUNCTIONALITY ───────────────────────────────── **/
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

function initSearchBinding() {
  const searchInput = document.getElementById("searchInput");
  if (!searchInput) return;

  if (document.querySelector(".summary-card")) {
    searchInput.addEventListener("input", filterCards);
  } else if (document.querySelector("td")) {
    enableTableSearch();
  }
}

/*** ─── SUGGESTIONS BOX ────────────────────────────────────── **/
function setupSuggestionBox() {
  const form = document.getElementById("suggestionForm");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = document.getElementById("suggestionInput");
    const status = document.getElementById("suggestionStatus");
    const suggestion = input.value.trim();
    if (!suggestion) return;

    try {
      const res = await fetch("http://127.0.0.1:8000/api/suggest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ suggestion })
      });
      if (res.ok) {
        status.textContent = "✅ Sent!";
        input.value = "";
      } else {
        status.textContent = "❌ Error sending";
      }
    } catch {
      status.textContent = "❌ Connection failed";
    }
  });
}

/*** ─── UTILS / INIT ───────────────────────────────────────── **/
document.addEventListener("DOMContentLoaded", () => {
  loadBuzzwords();
  loadRapidReviewCards();
  initSearchBinding();
  resizeCarouselFont();
  window.addEventListener("resize", resizeCarouselFont);

  // Suggestions box support
  setupSuggestionBox();
});