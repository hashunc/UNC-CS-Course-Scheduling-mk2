const editItems = document.getElementById('prof-edit-table');
let courses = [];
let availabilities = [['MWF', 1], ['MWF', 2], ['MWF', 3], ['MWF', 4], ['MWF', 5], ['MWF', 6], ['MWF', 7], 
['TTH', 1], ['TTH', 2], ['TTH', 3], ['TTH', 4], ['TTH', 5], ['TTH', 6], ['TTH', 7], ['TTH', 8],
['MW', 1], ['MW', 3], ['MW', 5], ['MW', 7]]


let original_data = [];

let q_courses_to_add = [];

let q_courses_to_remove = [];

let max_courses_to_change = [];

let mp_to_add = [];

let mp_to_remove = [];

function valid_availability(large_list, a){
    for(let availability of large_list){
        if(availability[0] === a[0] & availability[1] === a[1]){
            return true;
        }
    }
    return false;
}

// Fetch all courses
fetch('http://127.0.0.1:8000/courses')
    .then(response => response.json())
    .then(data => {
        courses = Object.keys(data);
    })

// Fetch all professors
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

                availability_item.querySelector('input').addEventListener('change', (event) => {
                    handleTimeChange(prof, availability[0], availability[1], event.target.checked);
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

            let delete_div = document.createElement('div');
            delete_div.className = 'delete-div';

            let delete_button = document.createElement('button');
            let reset_button = document.createElement('button');
            delete_button.innerText = 'Delete';
            //reset_button.innerText = 'Reset';

            delete_div.appendChild(delete_button);
            //delete_div.appendChild(reset_button);
            //reset_button.className = 'reset-button';

            // Check if max number of courses has been changed
            const input_field = max_input_div.firstChild.nextSibling;
            input_field.addEventListener('change', (event) => {
                console.log("Current List of Max Vals: ", max_courses_to_change);
                const max_val = event.target.value;
                if(max_courses_to_change.some((entry) => entry.Professor === prof)) {
                    console.log(max_courses_to_change.findIndex((entry) => entry.Professor === prof));
                    const index = max_courses_to_change.findIndex((entry) => entry.Professor === prof)
                    max_courses_to_change[index].Max = max_val
                } else {
                    max_courses_to_change.push({
                        Professor: prof,
                        Max: max_val
                    })
                }
                console.log("Input value changed for: ", event.target.value);
            })

            // reset_button.addEventListener('click', () => {
            //     console.log("Was clicked", prof);
            //     const profData = original_data[prof];
            //     max_input.value = profData['max_classes'];
            //     const originalQualifiedCourses = profData['qualified_courses'];
            //     const checkboxInputs = courses_scrollable.querySelectorAll('input[type="checkbox"]');
            //     checkboxInputs.forEach(checkbox => {
            //         const label = checkbox.nextSibling;
            //         const courseName = label.textContent;


            //         //Note: This code was works, but it fails to reset it back to the original settings after a course is deleted from qualified courses list in the DB
            //         //Instead, just reselect the course and hit submit
            //         var wasChecked
            //         if(checkbox.checked) {
            //             wasChecked = true
            //         } else {
            //             wasChecked = false
            //         }
            //         //checkbox.checked = originalQualifiedCourses.includes(courseName);
            //         const new_q_course = {
            //             Professor: prof,
            //             Course: courseName
            //         }
            //         console.log(new_q_course);

            //         if(!originalQualifiedCourses.includes(courseName) & wasChecked) {
            //             deleteQualCourse(new_q_course, prof)
            //         } 
            //         //Else if the course WAS originally qualified, but it is was unchecked: READD to DB
            //         else if(originalQualifiedCourses.includes(courseName) & !wasChecked) {
            //             addQualCourse(new_q_course)
            //         }
            //     });

            //     const originalAvailability = profData['availability'];
            //     const availabilityCheckboxInputs = availability_scrollable.querySelectorAll('input[type="checkbox"]');
            //     availabilityCheckboxInputs.forEach(checkbox => {
            //         const label = checkbox.nextSibling;
            //         const [days, timeSlotStr] = label.textContent.split(' ');
            //         const timeSlot = parseInt(timeSlotStr, 10);

            //         checkbox.checked = valid_availability(originalAvailability, [days, timeSlot]);
            //     });
            // });

            // delete_button.addEventListener('click', () => {
            //     const confirmation = confirm(`Are you sure you want to delete data for ${prof}?`);
            //     if (confirmation) {
            //         // Remove the professor's div from the DOM
            //         // list_item.remove();

            //         console.log('Working!');
            //     }
            // });

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
    console.log("Current Courses to Add: ", q_courses_to_add);
    console.log("Current Courses to Remove: ", q_courses_to_remove);
    console.log("Current MP to Add: ", mp_to_add);
    console.log("Current MP to Remove: ", mp_to_remove);

    //CALL API ROUTES
    if(q_courses_to_add.length > 0) {
        q_courses_to_add.forEach((q_course) => {
            addQualCourse(q_course);
        })
    }
    if(q_courses_to_remove.length > 0) {
        q_courses_to_remove.forEach((q_course) => {
            deleteQualCourse(q_course, q_course.Professor);
        })
    }
    if(max_courses_to_change.length > 0) {
        max_courses_to_change.forEach((max_course) => {
            const the_max = max_course.Max;
            const prof = max_course.Professor;
            updateMaxCourse(prof, the_max);
        })
    }
    if(mp_to_add.length > 0) {
        mp_to_add.forEach((availability) => {
            const prof = availability.Professor;
            const mp = availability.Meeting_Pattern;
            const period = availability.Period;
            addMp(prof, mp, period);
        })
    }
    if(mp_to_remove.length > 0) {
        mp_to_remove.forEach((availability) => {
            const prof = availability.Professor;
            const mp = availability.Meeting_Pattern;
            const period = availability.Period;
            deleteMp(prof, mp, period);
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

buttons_div.appendChild(back_button);
buttons_div.appendChild(submit_button);


function handleCourseChange(professor, course, adding) {

    //Define q_course to be an object with professor name and course they can teach
    const q_course = {
        Professor: professor,
        Course: course
    }

    //Check if we're adding or removing a course
    if (adding) {
    // If the course is scheduled to be removed, cancel it and move to courses to add
        if (q_courses_to_remove.some((entry) => entry.Professor === professor && entry.Course === course)) {
            console.log(`Course ${course} for Professor ${professor} moved from removal to addition.`);
            deleteFromList(q_courses_to_remove, q_course);
        }
        if (!q_courses_to_add.some((entry) => entry.Professor === professor && entry.Course === course)) {
            // Otherwise, schedule it to be added if it's not already in the add list
            q_courses_to_add.push(q_course);
            console.log(`Course ${course} for Professor ${professor} scheduled to be added.`);
        }
    } else {
    // If the course is scheduled to be added, cancel it and move to courses to remove
        if (q_courses_to_add.some((entry) => entry.Professor === professor && entry.Course === course)) {
            console.log(`Course ${course} for Professor ${professor} moved from addition to removal.`);
            deleteFromList(q_courses_to_add, q_course);
        }
        if (!q_courses_to_remove.some((entry) => entry.Professor === professor && entry.Course === course)) {
            // Otherwise, schedule it to be removed if it's not already in the remove list
            q_courses_to_remove.push(q_course);
            console.log(`Course ${course} for Professor ${professor} scheduled to be removed.`);
        }
    }
}


function handleTimeChange(professor, meeting_pattern, period, adding) {

    //Define q_course to be an object with professor name and course they can teach
    const mp = {
        Professor: professor,
        Meeting_Pattern: meeting_pattern,
        Period: period
    }
    //Check if we're adding or removing a course
    if (adding) {
    // If the course is scheduled to be removed, cancel it and move to courses to add
        if (mp_to_remove.some((entry) => entry.Professor === professor && entry.Meeting_Pattern === meeting_pattern && entry.Period === period)) {
            console.log(`Meeting Pattern ${meeting_pattern} at period ${period} for Professor ${professor} moved from removal to addition.`);
            deleteFromList(mp_to_remove, mp);
        }
        if (!mp_to_add.some((entry) => entry.Professor === professor && entry.Meeting_Pattern === meeting_pattern && entry.Period === period)) {
            // Otherwise, schedule it to be added if it's not already in the add list
            mp_to_add.push(mp);
            console.log(`Meeting Pattern ${meeting_pattern} at period ${period} for Professor ${professor} scheduled to be added.`);
        }
    } else {
    // If the course is scheduled to be added, cancel it and move to courses to remove
        if (mp_to_add.some((entry) => entry.Professor === professor && entry.Meeting_Pattern === meeting_pattern && entry.Period === period)) {
            console.log(`Meeting Pattern ${meeting_pattern} at period ${period} for Professor ${professor} moved from addition to removal.`);
            deleteFromList(mp_to_add, mp);
        }
        if (!mp_to_remove.some((entry) => entry.Professor === professor && entry.Meeting_Pattern === meeting_pattern && entry.Period === period)) {
            // Otherwise, schedule it to be removed if it's not already in the remove list
            mp_to_remove.push(mp);
            console.log(`Meeting Pattern ${meeting_pattern} at period ${period} for Professor ${professor} scheduled to be removed.`);
        }
    }
}


//Methods to call endpoints
function addQualCourse(payload) {
    fetch("http://127.0.0.1:8000/qualified", {
        method: 'POST',
        body: JSON.stringify(payload),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if(response.ok) {
            console.log("Added the Course: ", response);
            q_courses_to_add = []
        } else {
            console.log("Paylod could not send: ", payload);
            console.log("ERROR COULD NOT ADD THIS AS A QUALIFIED COURSE");
        }
    })
}

function deleteQualCourse(payload, professor) {
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
            q_courses_to_remove = []
        } else {
            console.log("Paylod could not send: ", payload);
            console.log("ERROR COULD NOT REMOVE THIS QUALIFIED COURSE");
        }
    })
}

function updateMaxCourse(professor, max) {
    fetch(`http://127.0.0.1:8000/max/${professor}?new_max=${max}`, {
        method: 'PUT'
    })
    .then(response => {
        if(response.ok) {
            console.log("Updated professor max", response);
            max_courses_to_change = []
        } else {
            console.log("Max courses couldn't be updated", response);
        }
    })
}
function addMp(professor, meeting_pattern, period) {
    fetch(`http://127.0.0.1:8000/availability/${professor}?AvailableMp=${meeting_pattern}&AvailablePeriod=${period}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if(response.ok) {
            console.log("Added the Mp: ", response);
            mp_to_add = []
        } else {
            console.log("Paylod could not send: ", payload);
            console.log("ERROR COULD NOT ADD THIS AS AVAILABILITY");
        }
    })
}

function deleteMp(professor, meeting_pattern, period) {
    fetch(`http://127.0.0.1:8000/availability/${professor}?AvailableMp=${meeting_pattern}&AvailablePeriod=${period}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if(response.ok) {
            console.log("Deleted the Mp: ", response);
            mp_to_remove = []
        } else {
            console.log("Paylod could not send: ", payload);
            console.log("ERROR COULD NOT REMOVE THIS AVAILABILITY");
        }
    })
}






// Helper function to remove an item from a list
function deleteFromList(list, item) {
    var index = -1
    index = list.findIndex(
        (entry) => entry.professor === item.professor && entry.course === item.course
    );
    console.log(index);
    if (index > -1) {
        list.splice(index, 1);
    }
}