


function toggleColumn(colIndex) {
  document.querySelectorAll('[data-col="' + colIndex + '"]').forEach(cell => {
    cell.style.display = (cell.style.display === 'none') ? '' : 'none';
  });
}

function resetColumns() {
  document.querySelectorAll('td, th').forEach(cell => {
    cell.style.display = '';
  });
}

function filterCards() {
  const input = document.getElementById("searchInput").value.toLowerCase();
  const rows = document.querySelectorAll(".autoantibody-table tbody tr");
  rows.forEach(row => {
    const text = row.textContent.toLowerCase();
    row.style.display = text.includes(input) ? "" : "none";
  });
}