let clicked = [];

function deleteFromClicked(string_in){
    let i = 0;
    while(i < clicked.length){
        if(clicked[i] === string_in){
            clicked = clicked.splice(i, i);
            break;
        }
        i += 1;
    }
}

fetch('http://127.0.0.1:8000')
  .then(response => response.json()
  )
  .then(data => {
    data = data['schedule'];
    console.log(data);

    const board = document.getElementById('update-course-board');
    data.forEach(element => {
        let small_div = document.createElement('div');
        small_div.innerText = `Course: ${element['Course']}\n
                                Section: ${element['Section']}\n
                                Title: ${element['Title']}\n
                                Professor: ${element['Professor']}\n
                                Start Time: ${element['Start Time']}`;
        small_div.className = 'update-small-div';
        let checker = document.createElement('input');
        checker.type = 'checkbox';
        checker.className = 'update-list-check';
        checker.dataset.course = element['Course']
        checker.dataset.section = element['Section']
        checker.dataset.title = element['Title']
        checker.dataset.prof = element['Professor']
        checker.dataset.start = element['Start Time']

        checker.addEventListener('click', () => {
            if(checker.checked){
                console.log(`${checker.dataset.course} ${checker.dataset.section} added!`)
                clicked.push(`${checker.dataset.course} ${checker.dataset.section}`);
            } else {
                console.log(`${checker.dataset.course} ${checker.dataset.section} removed!`)
                deleteFromClicked(`${checker.dataset.course} ${checker.dataset.section}`);
            }
            console.log(clicked);
        });

        board.appendChild(small_div);
        board.appendChild(checker);
    });
  });