// Shamelessly stolen from https://www.w3schools.com/howto/howto_js_sort_table.asp :^)
function sortTable(n) {
  let table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("gen-stats");
  switching = true;
  dir = "asc";
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      const xCtn = (n === 1 || n === 2) ? parseFloat(x.innerHTML) : x.innerHTML.toLowerCase();
      const yCtn = (n === 1 || n === 2) ? parseFloat(y.innerHTML) : y.innerHTML.toLowerCase();
      if (dir == "asc") {
        if (xCtn > yCtn) {
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (xCtn < yCtn) {
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount ++;
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
