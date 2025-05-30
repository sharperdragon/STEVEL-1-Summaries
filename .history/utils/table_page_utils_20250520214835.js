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

/**
 * Filter table rows based on input text (case insensitive)
 * @param {string} inputId - The ID of the text input
 * @param {string} tableSelector - CSS selector to target table(s)
 */
function filterTableRowsByInput(inputId, tableSelector) {
  const input = document.getElementById(inputId);
  const query = input.value.toLowerCase();
  document.querySelectorAll(`${tableSelector} tbody tr`).forEach(row => {
    const text = row.textContent.toLowerCase();
    row.style.opaciy = text.includes(query) ? '' : '0';
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
  const searchBox = document.getElementById("searchBox");
  if (searchBox) {
    searchBox.addEventListener("input", () => {
      filterTableRowsByInput("searchBox", "table");
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