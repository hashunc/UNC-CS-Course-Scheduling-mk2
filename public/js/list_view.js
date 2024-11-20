import { data } from './sample_data.js';

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

    cell0.innerHTML = element['course_number'];
    cell1.innerHTML = element['section'];
    cell2.innerHTML = element['title'];
    cell3.innerHTML = element['professor'];
    cell4.innerHTML = element['time_slot'];
    idx += 1;
});