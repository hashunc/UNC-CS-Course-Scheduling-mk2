const items = JSON.parse(localStorage.getItem('selectedItems') || '[]');

console.log(items);

const editList = document.getElementById('list-edit-table');
items.forEach(item => {
    const listItem = document.createElement('div');
    listItem.innerText = `${item['Title']} Sec. ${item['Section']}`;
    const keys = Object.keys(item);

    const params = document.createElement('div');
    listItem.appendChild(params);
    keys.forEach(key => {
        const divInputs = document.createElement('div');
        divInputs.innerText = key;

        const newInput = document.createElement('input');
        newInput.value = item[key];
        divInputs.appendChild(newInput);
        params.appendChild(divInputs);
    });
    
    editList.appendChild(listItem);
});

const return_div = document.getElementById('return-to-update-by-list');
let back_button = document.createElement('button');
back_button.innerText = 'Return';

back_button.addEventListener('click', () => {
    window.location.href = `list_update.html`;
});

back_button.class = 'return-button';
return_div.appendChild(back_button);
//document.appendChild(return_div);