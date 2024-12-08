const editItems = document.getElementById('prof-edit-table');
let courses = [];
let availabilities = [['MWF', 1], ['MWF', 2], ['MWF', 3], ['MWF', 4], ['MWF', 5], ['MWF', 6], ['MWF', 7], 
['TTH', 1], ['TTH', 2], ['TTH', 3], ['TTH', 4], ['TTH', 5], ['TTH', 6], ['TTH', 7], ['TTH', 8],
['MW', 1], ['MW', 3], ['MW', 5], ['MW', 7]]


let original_data = [];

function valid_availability(large_list, a){
    for(let availability of large_list){
        if(availability[0] === a[0] & availability[0] === a[0]){
            return true;
        }
    }
    return false;
}

fetch('http://127.0.0.1:8000/courses')
    .then(response => response.json())
    .then(data => {
        courses = Object.keys(data);
    })

fetch('http://127.0.0.1:8000/professors')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        original_data = data;
        for(let prof of Object.keys(data)){
            const list_item = document.createElement('div');
            list_item.className = 'edit-list-item';

            const title = document.createElement('div');
            title.innerText = `${prof}`;
            title.className = 'list-item-title';
            list_item.appendChild(title);

            const courses_scrollable = document.createElement('div');
            courses_scrollable.className = 'scrollable-element';

            const course_titles = document.createElement('div');
            course_titles.className = 'prof-edit-section';
            course_titles.innerText = 'Courses';
            list_item.appendChild(course_titles);

            for(let course of courses){
                let course_item = document.createElement('div')

                let course_item_input = document.createElement('input');
                course_item_input.type = 'checkbox';
                course_item.value = `${course}`;

                const label = document.createElement('label');
                label.textContent = course;

                courses_scrollable.appendChild(course_item);

                if(data[prof]['qualified_courses'].includes(course)){
                    course_item_input.checked = true;
                }

                course_item.appendChild(course_item_input);
                course_item.appendChild(label);
            }

            const available_titles = document.createElement('div');
            available_titles.className = 'prof-edit-section';
            available_titles.innerText = 'Availability';

            const availability_scrollable = document.createElement('div');
            availability_scrollable.className = 'scrollable-element';

            for(let availability of availabilities){
                console.log(availability);
                console.log(data[prof]['availability'])
                let availability_item = document.createElement('div')

                let availability_item_input = document.createElement('input');
                availability_item_input.type = 'checkbox';

                const label = document.createElement('label');
                label.textContent = `${availability[0]} ${availability[1]}`;

                availability_scrollable.appendChild(availability_item);

                if(valid_availability(data[prof]['availability'], availability)){
                    availability_item_input.checked = true;
                }

                availability_item.appendChild(availability_item_input);
                availability_item.appendChild(label);
            }

            let max_input_div = document.createElement('div')
            max_input_div.className = 'max-courses';

            const max_label = document.createElement('label');
            max_label.textContent = 'Max Courses:';

            let max_input = document.createElement('input');
            max_input.value = `${data[prof]['max_classes']}`;
            max_input.className = 'max-course-input';
            max_input.type = 'number';

            max_input_div.appendChild(max_label);
            max_input_div.appendChild(max_input);

            let delete_div = document.createElement('div');
            delete_div.className = 'delete-div';

            let delete_button = document.createElement('button');
            let reset_button = document.createElement('button');
            delete_button.innerText = 'Delete';
            reset_button.innerText = 'Reset';

            delete_div.appendChild(delete_button);
            delete_div.appendChild(reset_button);
            reset_button.className = 'reset-button';

            reset_button.addEventListener('click', () => {
                const profData = original_data[prof];
                max_input.value = profData['max_classes'];
                const originalQualifiedCourses = profData['qualified_courses'];
                const checkboxInputs = courses_scrollable.querySelectorAll('input[type="checkbox"]');
                checkboxInputs.forEach(checkbox => {
                    const label = checkbox.nextSibling;
                    const courseName = label.textContent;
                    checkbox.checked = originalQualifiedCourses.includes(courseName);
                });

                const originalAvailability = profData['availability'];
                const availabilityCheckboxInputs = availability_scrollable.querySelectorAll('input[type="checkbox"]');
                availabilityCheckboxInputs.forEach(checkbox => {
                    const label = checkbox.nextSibling;
                    const [days, timeSlotStr] = label.textContent.split(' ');
                    const timeSlot = parseInt(timeSlotStr, 10);

                    checkbox.checked = valid_availability(originalAvailability, [days, timeSlot]);
                });
            });

            delete_button.addEventListener('click', () => {
                const confirmation = confirm(`Are you sure you want to delete data for ${prof}?`);
                if (confirmation) {
                    // Remove the professor's div from the DOM
                    // list_item.remove();

                    console.log('Working!');
                }
            });

            list_item.appendChild(courses_scrollable);
            list_item.appendChild(available_titles);
            list_item.appendChild(availability_scrollable);
            list_item.appendChild(max_input_div);
            list_item.appendChild(delete_div);
            editItems.appendChild(list_item);
        }
    })

const buttons_div = document.getElementById('return-to-update-by-list');
let back_button = document.createElement('button');
let submit_button = document.createElement('button');

back_button.innerText = 'Return';
submit_button.innerText = 'Submit';

back_button.addEventListener('click', () => {
    window.location.href = `edit_fields.html`;
});

submit_button.addEventListener('click', () => {
    if(validate()){
        console.log('WAHOO!');
    }
});

function validate() {
    return true;
}

buttons_div.className = 'list-edit-bottom';

buttons_div.appendChild(back_button);
buttons_div.appendChild(submit_button);