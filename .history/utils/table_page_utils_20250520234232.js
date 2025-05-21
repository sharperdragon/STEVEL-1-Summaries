/**
 * Toggle visibility of a given column index across all tables
 */
function toggleColumn(colIndex) {
  document.querySelectorAll('td[data-col="' + colIndex + '"]').forEach(cell => {
    cell.style.opacity = (cell.style.opacity === '0') ? '' : '0';
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

document.addEventListener("DOMContentLoaded", () => {
  const resetBtn = document.getElementById("resetButton");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      resetColumns();
    });
  }

  const searchInput = document.getElementById("searchInput");
  if (searchInput && document.querySelector("table")) {
    searchInput.addEventListener("input", () => {
      const query = searchInput.value.toLowerCase();
      document.querySelectorAll("td").forEach(cell => {
        const text = cell.textContent.toLowerCase();
        cell.style.opacity = text.includes(query) ? "" : "0.2";
      });
    });
  }

  document.querySelectorAll("table tbody tr").forEach(row => {
    row.addEventListener("click", () => {
      row.querySelectorAll("td").forEach(cell => {
        if (cell.style.opacity === "0") {
          cell.style.opacity = "";
        }
      });
    });
  });
});