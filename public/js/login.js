const loginButton = document.getElementById("password-submit-button");
const inputtedPassword = document.getElementById('password-insert');

loginButton.addEventListener('click', () => {
    if(inputtedPassword.value === 'unccompscheduler'){
        window.location.href = "home.html";
    } else if(inputtedPassword.value != '') {
        alert('Incorrect password, please try again.')
    }
});