fetch('http://127.0.0.1:8000')
  .then(response => response.json()
  )
  .then(data => {
    data = data['schedule'];
    console.log(data);
    const tableDiv = document.getElementById('list-view');

    tableDiv.style.marginTop = '20px';

    tableDiv.innerHTML = `
    <table style="width:100%" id="list-table">
    <tr>
      <th>Course Number</th>
      <th>Section</th>
      <th>Course Title</th>
      <th>Professor</th>
      <th>Time Slot</th>
    </tr>
    </table>
    `;

    const table = document.getElementById('list-table');

    let idx = 1
    data.forEach(element => {
        var row = table.insertRow(idx);
        var cell0 = row.insertCell(0);
        var cell1 = row.insertCell(1);
        var cell2 = row.insertCell(2);
        var cell3 = row.insertCell(3);
        var cell4 = row.insertCell(4);

        cell0.innerHTML = element['Course'];
        cell1.innerHTML = element['Section'];
        cell2.innerHTML = element['Title'];
        cell3.innerHTML = element['Professor'];
        cell4.innerHTML = element['Start Time'];
        idx += 1;
    });
  });