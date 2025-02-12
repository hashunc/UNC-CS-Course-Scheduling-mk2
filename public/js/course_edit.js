const editItems = document.getElementById('course-edit-table');
let courses = [];

let original_data = [];

let courses_to_update = []; //PUT {course-section} Used to update section or max capacity of an existing course

let courses_to_remove = []; //DELETE {course-section} Used to remove section of an course

let courses_to_add = []; //POST {course (JSON Body)} Used to add a new course/section of a course


fetch('http://127.0.0.1:8000/courses')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        original_data = data;
        for(let course of Object.keys(data)){
            const list_item = document.createElement('div');
            list_item.className = 'edit-list-item';

            const title = document.createElement('div');
            title.innerText = `${course}`;
            title.className = 'list-item-title';
            list_item.appendChild(title);

            const course_section_div = document.createElement('div');
            course_section_div.className = 'center-table';
            const course_section_table = document.createElement('table');
            course_section_table.className = 'format-course-table'

            const headerRow = course_section_table.createTHead().insertRow();
            const headers = ['Section', 'Max Capacity', ' '];

            headers.forEach(headerText => {
                const headerCell = document.createElement("th");
                headerCell.textContent = headerText;
                headerCell.className = 'course-th-column';
                headerRow.appendChild(headerCell);
            });

            function renderTableRows() {
                // Remove all rows except the header
                while (course_section_table.rows.length > 1) {
                    course_section_table.deleteRow(1);
                }
        
                // Re-insert rows from original_data for this course
                let sections = original_data[course]['sections'];
                for (let section of sections) {
                    const newRow = course_section_table.insertRow(-1);
                    const cell0 = newRow.insertCell(0);
                    const cell1 = newRow.insertCell(1);
                    const cell2 = newRow.insertCell(2);
        
                    const cell0_input = document.createElement('input');
                    const cell1_input = document.createElement('input');
        
                    cell0_input.type = 'number';
                    cell0_input.value = section['section_number'];
                    cell0_input.className = 'narrow-input';
        
                    cell1_input.type = 'number';
                    cell1_input.value = section['seat_capacity'];
                    cell1_input.className = 'narrow-input';
        
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
            }

            renderTableRows();



            let delete_div = document.createElement('div');
            delete_div.className = 'delete-div';

            let add_section_button = document.createElement('button');
            add_section_button.innerText = 'Add Section'

            add_section_button.addEventListener('click', () => {
                const newRow = course_section_table.insertRow(-1);
            
                const cell0 = newRow.insertCell(0);
                const cell1 = newRow.insertCell(1);
                const cell2 = newRow.insertCell(2);
            
                const cell0_input = document.createElement('input');
                cell0_input.type = 'number';
                cell0_input.value = '';
                cell0_input.className = 'narrow-input';
            
                const cell1_input = document.createElement('input');
                cell1_input.type = 'number';
                cell1_input.value = '';
                cell1_input.className = 'narrow-input';
            
                const delete_section_button = document.createElement('button');
                delete_section_button.innerText = 'Delete';
                delete_section_button.addEventListener('click', () => {
                    course_section_table.deleteRow(newRow.rowIndex);
                });
            
                // Append inputs and button to cells
                cell0.appendChild(cell0_input);
                cell1.appendChild(cell1_input);
                cell2.appendChild(delete_section_button);
            });

            let delete_button = document.createElement('button');
            let reset_button = document.createElement('button');
            delete_button.innerText = 'Delete Course';
            reset_button.innerText = 'Reset';
            reset_button.addEventListener('click', () => {
                renderTableRows();
            });

            delete_button.addEventListener('click', () => {
                const confirmation = confirm(`Are you sure you want to delete data for ${course}?`);
                if (confirmation) {
                    // Remove the courses's div from the DOM
                    // list_item.remove();
                    console.log('Working!');
                }
            });

            delete_div.appendChild(add_section_button);
            delete_div.appendChild(delete_button);
            delete_div.appendChild(reset_button);
            delete_button.className = 'reset-button'
            reset_button.className = 'reset-button';

            course_section_div.appendChild(course_section_table);
            list_item.appendChild(course_section_div);
            list_item.appendChild(course_section_div);
            list_item.appendChild(delete_div);
            editItems.appendChild(list_item);
        }
    })

const buttons_div = document.getElementById('return-to-update-by-list');
let add_course_button = document.createElement('button');
let back_button = document.createElement('button');
let submit_button = document.createElement('button');

add_course_button.innerText = 'Add Course';
back_button.innerText = 'Return';
submit_button.innerText = 'Submit';

add_course_button.addEventListener('click', () => {
    window.location.href = `add_new_course.html`;
});

back_button.addEventListener('click', () => {
    window.location.href = `edit_fields.html`;
});

submit_button.addEventListener('click', () => {
    if(courses_to_update.length > 0) {
        courses_to_update.forEach((coursePayload) => {
            updateCourses(coursePayload);
        })
    }
    if(validate()){
        console.log('WAHOO!');
    }
});

function validate() {
    return true;
}

buttons_div.className = 'list-edit-bottom';

buttons_div.appendChild(add_course_button);
buttons_div.appendChild(back_button);
buttons_div.appendChild(submit_button);