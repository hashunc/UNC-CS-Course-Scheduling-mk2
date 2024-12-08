const item = document.getElementById('rooms-edit-table');
let original_data = null;

fetch('http://127.0.0.1:8000/rooms')
    .then(response => response.json())
    .then(data => {
        original_data = data;
        console.log(data);
        const insert_class_div = document.createElement('div');
        insert_class_div.className = 'edit-list-item';

        const rooms_table_div = document.createElement('div');
        rooms_table_div.className = 'general-center';
        const rooms_table = document.createElement('table');
        rooms_table.className = 'format-course-table'

        const headerRow = rooms_table.createTHead().insertRow();
        const headers = ['Room', 'Max Occupancy', ''];

        headers.forEach(headerText => {
            const headerCell = document.createElement("th");
            headerCell.textContent = headerText;
            headerCell.className = 'course-th-column';
            headerRow.appendChild(headerCell);
        });

        for(let room of Object.keys(data)){
            const newRow = rooms_table.insertRow(-1);
            const cell0 = newRow.insertCell(0);
            const cell1 = newRow.insertCell(1);
            const cell2 = newRow.insertCell(2);

            const cell0_input = document.createElement('input');
            const cell1_input = document.createElement('input');

            cell0_input.value = room;
            cell0_input.style.width = '80px';

            cell1_input.type = 'number';
            cell1_input.value = data[room]['capacity'];
            cell1_input.style.width = '60px';

            const delete_section_button = document.createElement('button');
            delete_section_button.innerText = 'Delete';
            delete_section_button.addEventListener('click', () => {
                console.log('Will delete!')
                //course_section_table.deleteRow(newRow.rowIndex);
            });

            cell0.appendChild(cell0_input);
            cell1.appendChild(cell1_input);
            cell2.appendChild(delete_section_button);
        }

        const buttons_div = document.createElement('div');
        const add_room = document.createElement('button');
        add_room.innerText = 'Add Room';
        const reset = document.createElement('button');
        reset.innerText = 'Reset'
        const submit = document.createElement('button');
        submit.innerText = 'Submit';

        add_room.addEventListener('click', () => {
            const newRow = rooms_table.insertRow(-1);
        
            const cell0 = newRow.insertCell(0);
            const cell1 = newRow.insertCell(1);
            const cell2 = newRow.insertCell(2);
        
            const cell0_input = document.createElement('input');
            cell0_input.type = 'text';
            cell0_input.style.width = '80px';
            cell0_input.value = '';
        
            const cell1_input = document.createElement('input');
            cell1_input.type = 'number';
            cell1_input.style.width = '60px';
            cell1_input.value = '';
        
            const delete_section_button = document.createElement('button');
            delete_section_button.innerText = 'Delete';
            delete_section_button.addEventListener('click', () => {
                rooms_table.deleteRow(newRow.rowIndex);
            });
        
            cell0.appendChild(cell0_input);
            cell1.appendChild(cell1_input);
            cell2.appendChild(delete_section_button);
        });

        reset.addEventListener('click', () => {
            while (rooms_table.rows.length > 1) {
                rooms_table.deleteRow(1);
            }

            for (let room of Object.keys(original_data)) {
                const newRow = rooms_table.insertRow(-1);
                const cell0 = newRow.insertCell(0);
                const cell1 = newRow.insertCell(1);
                const cell2 = newRow.insertCell(2);
        
                const cell0_input = document.createElement('input');
                const cell1_input = document.createElement('input');
                
                cell0_input.value = room;
                cell0_input.style.width = '80px';
        
                cell1_input.type = 'number';
                cell1_input.value = original_data[room]['capacity'];
                cell1_input.style.width = '60px';
        
                const delete_section_button = document.createElement('button');
                delete_section_button.innerText = 'Delete';
                delete_section_button.addEventListener('click', () => {
                    rooms_table.deleteRow(newRow.rowIndex);
                });
        
                cell0.appendChild(cell0_input);
                cell1.appendChild(cell1_input);
                cell2.appendChild(delete_section_button);
            }
        });

        submit.addEventListener('click', () => {
            // Need to fill out with correct endpoint and redirect
        });

        buttons_div.className = 'general-center';
        buttons_div.style.marginTop = '20px';

        reset.style.marginLeft = '20px';
        submit.style.marginLeft = '20px';

        buttons_div.appendChild(add_room);
        buttons_div.appendChild(reset);
        buttons_div.appendChild(submit);

        rooms_table_div.appendChild(rooms_table);
        insert_class_div.appendChild(rooms_table_div)
        insert_class_div.appendChild(buttons_div);
        item.appendChild(insert_class_div);
    });