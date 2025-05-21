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

document.addEventListener("DOMContentLoaded", () => {
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