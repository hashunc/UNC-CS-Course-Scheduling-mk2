fetch('http://127.0.0.1:8000')
  .then(response => response.json()
  )
  .then(data => {
    data = data['schedule'];
    console.log(data);

    const board = document.getElementById('update-course-board');
    // cell0.innerHTML = element['Course'];
    // cell1.innerHTML = element['Section'];
    // cell2.innerHTML = element['Title'];
    // cell3.innerHTML = element['Professor'];
    // cell4.innerHTML = element['Start Time'];
    data.forEach(element => {
        let small_div = document.createElement('div');
        small_div.innerText = `Course: ${element['Course']}\n
                                Section: ${element['Section']}\n
                                Title: ${element['Title']}\n
                                Professor: ${element['Professor']}\n
                                Start Time: ${element['Start Time']}`;
        small_div.className = 'update-small-div';
        board.appendChild(small_div);
    });
  });