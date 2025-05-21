function filterTableRows() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const rows = document.querySelectorAll("table tbody tr");

    rows.forEach(row => {
        const rowText = Array.from(row.querySelectorAll("td"))
            .map(td => td.textContent.toLowerCase())
            .join(" ");
        row.style.display = rowText.includes(input) ? "" : "none";
    });
}