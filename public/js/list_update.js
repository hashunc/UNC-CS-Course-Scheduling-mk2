let clicked = [];

function compareJSONs(json_1, json_2){
    let keys = Object.keys(json_1);
    for(let key of keys){
        if(json_1[key] != json_2[key]){
            return false;
        }
    }
    return true;
}

function deleteFromClicked(json_in){
    let i = 0;
    while(i < clicked.length){
        if(compareJSONs(clicked[i], json_in)){
            clicked.splice(i, 1);
            return;
        }
        i += 1;
    }
}

fetch('http://127.0.0.1:8000/schedule')
  .then(response => response.json())
  .then(data => {
    //data = data['schedule'];
    console.log(data);

    const board = document.getElementById('update-course-board');
    data.forEach(element => {
        let small_div = document.createElement('div');
        small_div.innerText = `Course: ${element['Course']}\n
                                Section: ${element['Section']}\n
                                Title: ${element['Title']}\n
                                Professor: ${element['Prof']}\n
                                Start Time: ${element['Start']}\n
                                Meeting Pattern: ${element['MeetingPattern']}\n
                                Seat Capacity: ${element['SeatCapacity']}\n
                                Room: ${element['Room']}\n`;
        small_div.className = 'update-small-div';
        let checker = document.createElement('input');
        checker.type = 'checkbox';
        checker.className = 'update-list-check';
        checker.dataset.course = element['Course'];
        checker.dataset.section = element['Section'];
        checker.dataset.title = element['Title'];
        checker.dataset.prof = element['Professor'];
        checker.dataset.start = element['Start Time'];
        checker.dataset.meeting = element['Meeting Pattern'];
        checker.dataset.seat = element['Seat Capacity'];
        checker.dataset.room = element['Room'];

        checker.addEventListener('click', () => {
            let course_data = {
                'Course': checker.dataset.course,
                'Section': checker.dataset.section,
                'Title': checker.dataset.title,
                'Prof': checker.dataset.prof,
                'Start': checker.dataset.start,
                'Meeting Pattern': checker.dataset.meeting,
                'Seat Capacity': checker.dataset.seat,
                'Room': checker.dataset.room
            }
            if(checker.checked){
                console.log(`${checker.dataset.course} ${checker.dataset.section} added!`)
                clicked.push(course_data);
            } else {
                console.log(`${checker.dataset.course} ${checker.dataset.section} removed!`)
                deleteFromClicked(course_data);
            }
            console.log(clicked);
        });

        board.appendChild(small_div);
        board.appendChild(checker);
    });
    let button_div = document.createElement('div');
    button_div.id = 'submit-button-box';
    let submit_button = document.createElement('button');
    submit_button.innerText = 'Submit';
    submit_button.id = 'update-list-submit';

    submit_button.addEventListener('click', () => {
        if(clicked.length === 0){
            alert('Please select at least 1 course to edit')
        } else {
            console.log(clicked);
            localStorage.setItem('selectedItems', JSON.stringify(clicked));
            window.location.href = `edit_by_list.html`
        }
    });

    board.appendChild(button_div);
    button_div.appendChild(submit_button);
  });