/**
 * Toggle visibility of a given column index across all tables
 */
function toggleColumn(colIndex) {
  const cells = document.querySelectorAll('td[data-col="' + colIndex + '"]');
  const currentlyHidden = Array.from(cells).every(cell => cell.dataset.hidden === "true");
  cells.forEach(cell => {
    if (currentlyHidden) {
      cell.style.opacity = "";
      delete cell.dataset.hidden;
    } else {
      cell.style.opacity = "0";
      cell.dataset.hidden = "true";
    }
  });
}

/**
 * Show all columns by resetting inline styles
 */
function resetColumns() {
  document.querySelectorAll('td, th').forEach(cell => {
    cell.style.opacity = '';
  });
}

function filterRowsByInput(inputId, rowSelector) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const query = input.value.toLowerCase();
  document.querySelectorAll(rowSelector).forEach(row => {
    const text = row.textContent.toLowerCase();
    row.style.opacity = text.includes(query) ? "" : "0";
  });
}

/**
 * Shuffle all rows inside all tbody sections of a table,
 * preserving section-divider rows at the start of each tbody.
 */
function shuffleTableRows(table) {
  const tbodies = table.querySelectorAll("tbody");
  tbodies.forEach(tbody => {
    const rows = Array.from(tbody.querySelectorAll("tr"))
      .filter(row => !row.classList.contains("section-divider"));
    const sectionRows = Array.from(tbody.querySelectorAll("tr.section-divider"));

    // Fisher-Yates shuffle
    for (let i = rows.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [rows[i], rows[j]] = [rows[j], rows[i]];
    }

    // Hide section headers before appending
    sectionRows.forEach(row => {
      row.style.display = "none";
    });

    // Clear and re-append only shuffled rows
    tbody.innerHTML = "";
    rows.forEach(row => tbody.appendChild(row));
  });
}

// Add shuffle button listener for all tables on the page
document.addEventListener("DOMContentLoaded", () => {
  const shuffleBtn = document.getElementById("shuffleButton");
  if (shuffleBtn) {
    shuffleBtn.addEventListener("click", () => {
      document.querySelectorAll("table").forEach(table => shuffleTableRows(table));
    });
  }

  const resetBtn = document.getElementById("resetButton");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      resetColumns();
    });
  }

  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      filterRowsByInput("searchInput", "tbody tr td");
    });
  }

  // Add click-to-restore on individual td cells
  document.querySelectorAll("td").forEach(cell => {
    cell.addEventListener("click", () => {
      cell.style.opacity = "";
    });
  });
});

document.querySelectorAll(".th-dropdown a").forEach(link => {
  link.addEventListener("click", (event) => {
    const colIndex = link.getAttribute("data-col");
    if (colIndex !== null) toggleColumn(colIndex);
    event.preventDefault();
  });
});

document.querySelectorAll(".th-menu-wrapper").forEach(wrapper => {
  const dropdown = wrapper.querySelector(".th-dropdown");
  if (!dropdown) return;

  let hideTimeout;

  const showDropdown = () => {
    clearTimeout(hideTimeout);
    dropdown.style.display = "block";
  };

  const hideDropdown = () => {
    hideTimeout = setTimeout(() => {
      dropdown.style.display = "none";
    }, 500); // 1 second delay
  };

  wrapper.addEventListener("mouseenter", showDropdown);
  wrapper.addEventListener("mouseleave", hideDropdown);
  dropdown.addEventListener("mouseenter", showDropdown);
  dropdown.addEventListener("mouseleave", hideDropdown);
});