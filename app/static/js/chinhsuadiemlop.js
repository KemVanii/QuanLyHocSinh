function deleteColumn(button, columnType) {
    const remainingColumns15p = countColumnsWithText('15p');
    const remainingColumns45p = countColumnsWithText('45p');
    if (columnType === '15p' && remainingColumns15p === 1)
       return alert("Số lượng cột tối thiểu của '15p' là 1.");
    if (columnType === '45p' && remainingColumns45p === 1)
    return alert("Số lượng cột tối thiểu của '45p' là 1.");

    var columnIndex = button.parentNode.cellIndex;
    var rows = document.querySelectorAll('tr');
    rows.forEach(function(row) {
        var cells = row.querySelectorAll('td, th');
        cells[columnIndex].remove();
    });
}

function countColumnsWithText(text) {
    var count = 0;
    var headerCells = document.querySelectorAll('thead tr th span');
    headerCells.forEach(function(cell) {
        if (cell.textContent.trim() === text) {
        count++;
        }
    });
    return count;
}

function add15pColumn() {
  // Get the table
   if (countColumnsWithText('15p') === 5)
       return alert("Số lượng cột tối đa của '15p' là 5.");
  var table = document.querySelector('.table'); // Replace 'your-table-id' with the actual ID of your table
    const last15pIndex = countColumnsWithText('15p') + 2;
  // Add a new header cell after the last "15p" column
  var newHeaderCell = document.createElement('th');
  newHeaderCell.className = 'text-center';
  newHeaderCell.innerHTML = `<span>15p</span> <button type="submit" class="ml-1 btn btn-secondary p-1" onclick="deleteColumn(this, '15p')">Xóa</button>`;
  if (last15pIndex !== -1) {
    var insertIndex = last15pIndex +1;
    table.rows[0].insertBefore(newHeaderCell, table.rows[0].cells[insertIndex]);
  } else {
    table.rows[0].appendChild(newHeaderCell);
  }

  // Add a new cell to each row after the last "15p" column
  var rows = table.getElementsByTagName('tr');
  for (var j = 1; j < rows.length; j++) {
    const scoreBoardId=rows[j].querySelector('input').value
    var newCell = document.createElement('td');
    newCell.innerHTML = `<input type="number" name="15p${scoreBoardId}[]" class="form-control border-0 form-control-sm" min="0" max="10" step="any" required>`;
    if (last15pIndex !== -1) {
      var insertIndex = last15pIndex + 1;
      rows[j].insertBefore(newCell, rows[j].cells[insertIndex]);
    } else {
      rows[j].appendChild(newCell);
    }
  }
}

function add45pColumn() {
  // Get the table
   if (countColumnsWithText('45p') === 3)
       return alert("Số lượng cột tối đa của '45p' là 3.");
  var table = document.querySelector('.table'); // Replace 'your-table-id' with the actual ID of your table
    const last15pIndex = countColumnsWithText('15p') + countColumnsWithText('45p') + 2;
  // Add a new header cell after the last "15p" column
  var newHeaderCell = document.createElement('th');
  newHeaderCell.className = 'text-center';
  newHeaderCell.innerHTML = `<span>45p</span> <button type="submit" class="ml-1 btn btn-secondary p-1" onclick="deleteColumn(this, '45p')">Xóa</button>`;
  if (last15pIndex !== -1) {
    var insertIndex = last15pIndex +1;
    table.rows[0].insertBefore(newHeaderCell, table.rows[0].cells[insertIndex]);
  } else {
    table.rows[0].appendChild(newHeaderCell);
  }

  // Add a new cell to each row after the last "15p" column
  var rows = table.getElementsByTagName('tr');
  for (var j = 1; j < rows.length; j++) {
    const scoreBoardId=rows[j].querySelector('input').value
    console.log(scoreBoardId)
    var newCell = document.createElement('td');
    newCell.innerHTML = `<input type="number" name="45p${scoreBoardId}[]" class="form-control border-0 form-control-sm" min="0" max="10" step="any" required>`;
    if (last15pIndex !== -1) {
      var insertIndex = last15pIndex + 1;
      rows[j].insertBefore(newCell, rows[j].cells[insertIndex]);
    } else {
      rows[j].appendChild(newCell);
    }
  }
}
