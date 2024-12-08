const editItems = document.getElementById('prof-edit-table');
let courses = [];

let original_data = [];

fetch('http://127.0.0.1:8000/courses')
    .then(response => response.json())
    .then(data => {
        courses = Object.keys(data);
        console.log(courses);
    })

fetch('http://127.0.0.1:8000/professors')
    .then(response => response.json())
    .then(data => {
        original_data = data;
        console.log(original_data);
        for(let prof of Object.keys(data)){
            const list_item = document.createElement('div');
            list_item.className = 'edit-list-item';

            const title = document.createElement('div');
            title.innerText = `${prof}`;
            title.className = 'list-item-title';
            list_item.appendChild(title);

            const courses_scrollable = document.createElement('div');
            courses_scrollable.className = 'scrollable-element';

            for(let course of courses){
                let course_item = document.createElement('div');
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
                course_item.querySelector('input').addEventListener('change', (event) => {
                    handleCourseChange(prof, course, event.target.checked);
                });
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

            list_item.appendChild(courses_scrollable);
            list_item.appendChild(max_input_div);
            editItems.appendChild(list_item);
        }
    })

function handleCourseChange(professor, course, adding) {
    console.log("HERE IS", professor, "Are they qualified for:", course, "? The answer is:", adding);
    const payload = {
        Professor: professor,
        Course: course
    }
    console.log("STRINGIFIED", JSON.stringify(payload));
    console.log(payload);
    if(adding) {
        fetch("http://127.0.0.1:8000/qualified", {
            method: 'POST',
            body: JSON.stringify(payload),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if(response.ok) {
                console.log("This happened: ", response);
            } else {
                console.log("Paylod could not send: ", payload);
                console.log("ERROR COULD NOT ADD THIS AS A QUALIFIED COURSE");
            }
        })
    } else {
        fetch(`http://127.0.0.1:8000/qualified/${professor}`, {
            method: 'DELETE',
            body: JSON.stringify(payload),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if(response.ok) {
                console.log("Deleted the Course: ", response);
            } else {
                console.log("Paylod could not send: ", payload);
                console.log("ERROR COULD NOT REMOVE THIS QUALIFIED COURSE");
            }
        })
    }
}