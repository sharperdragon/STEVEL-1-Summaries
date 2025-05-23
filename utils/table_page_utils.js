const originalTableState = new Map();

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
 * Reset visibility styles and restore original row order for all tables.
 */
function resetColumns() {
  document.querySelectorAll('td, th').forEach(cell => {
    cell.style.opacity = '';
  });

  document.querySelectorAll("table").forEach((table, tableIndex) => {
    const tbodies = table.querySelectorAll("tbody");
    const cachedRows = originalTableState.get(tableIndex);

    if (!cachedRows) return;

    tbodies.forEach((tbody, i) => {
      if (!cachedRows[i]) return;
      tbody.innerHTML = "";
      cachedRows[i].forEach(row => tbody.appendChild(row.cloneNode(true)));
    });
  });
}

function filterRowsByInput(inputId, rowSelector) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const query = input.value.toLowerCase();
  document.querySelectorAll(rowSelector).forEach(row => {
    if (row.closest("tfoot") || row.classList.contains("section-divider")) return;
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
      .filter(row => !row.classList.contains("section-divider") && !row.closest("tfoot"));
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

    // Clear tbody and re-append only shuffled rows
    tbody.innerHTML = "";
    rows.forEach(row => tbody.appendChild(row));
  });
}

// Add shuffle button listener for all tables on the page
document.addEventListener("DOMContentLoaded", () => {
  const shuffleBtn = document.getElementById("shuffle-button");
  if (shuffleBtn) {
    shuffleBtn.addEventListener("click", () => {
      document.querySelectorAll("table").forEach(table => shuffleTableRows(table));
    });
  }

  // Cache original table row order at load time to support reset
  document.querySelectorAll("table").forEach((table, tableIndex) => {
    const tbodies = table.querySelectorAll("tbody");
    const cachedTbodyRows = [];

    tbodies.forEach(tbody => {
      const rows = Array.from(tbody.querySelectorAll("tr"));
      cachedTbodyRows.push(rows.map(row => row.cloneNode(true)));
    });

    originalTableState.set(tableIndex, cachedTbodyRows);
  });

  const resetBtn = document.getElementById("reset-button");
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
    }, 400); //
  };

  wrapper.addEventListener("mouseenter", showDropdown);
  wrapper.addEventListener("mouseleave", hideDropdown);
  dropdown.addEventListener("mouseenter", showDropdown);
  dropdown.addEventListener("mouseleave", hideDropdown);
});