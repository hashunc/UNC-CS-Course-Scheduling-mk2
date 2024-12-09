let courses = [];

const item = document.getElementById('add-new-course');

fetch('http://127.0.0.1:8000/courses')
    .then(response => response.json())
    .then(data => {
        console.log(data)
        courses = Object.keys(data);
    });

const insert_class_div = document.createElement('div');
insert_class_div.className = 'edit-list-item';

const title = document.createElement('div');
title.className = 'general-center';
title.innerText = 'Enter Course Name Below:';
title.style.fontSize = '15px';

const insert_name_div = document.createElement('div');
const comp_course_number = document.createElement('input');

insert_name_div.appendChild(comp_course_number);
insert_name_div.className = 'general-center';
insert_name_div.style.marginTop = '20px';

const buttons_div = document.createElement('div');
buttons_div.className = 'general-center';
buttons_div.style.marginTop = '20px';
const return_button = document.createElement('button');
return_button.innerText = 'Return';

const submit_button = document.createElement('button');
submit_button.innerText = 'Submit';
submit_button.style.marginLeft = '20px';

buttons_div.appendChild(return_button);
buttons_div.appendChild(submit_button);

return_button.addEventListener('click', () => {
    window.location.href = `classes.html`;
});

submit_button.addEventListener('click', () => {
    if(courses.includes(comp_course_number.value)){
        alert('Course already included');
    } // Add some more validation measures
    else {
        // Call correct endpoint to insert course and redirect to classes.html
    }
});

insert_class_div.appendChild(title);
insert_class_div.appendChild(insert_name_div);
insert_class_div.appendChild(buttons_div);

item.appendChild(insert_class_div);