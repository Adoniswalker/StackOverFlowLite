let form = document.getElementById('signup');

if (form) {
    form.addEventListener("submit", create_user);
}

function create_user() {
    "use strict";
    event.preventDefault();
    fetch("/api/v1/auth/signup/", {
        method: "POST",
        mode: "cors",
        body: new FormData(form)
    })
        .then((res) => {
            res.json().then((data) => {
                if (res.status === 201) {
                    window.location.replace("/login")
                }
                else {
                    console.log(data["message"]["email"]);
                    changeHtml(data["message"]["email"], "email_error");
                    changeHtml(data["message"]["password"], "password_error");
                }
            });
        })
        .catch((err) => {
            console.log("Eror", err);
        });
}

let login_form = document.getElementById('login');

if (login_form) {
    login_form.addEventListener("submit", loginUser);
}

function loginUser() {
    "use strict";
    event.preventDefault();
    fetch("/api/v1/auth/login/", {
        method: "POST",
        mode: "cors",
        body: new FormData(login_form)
    })
        .then((res) => {
            res.json().then((data) => {
                if (res.status === 200) {
                         console.log(data);
               window.location.replace("/")
                }
                else if(res.status === 404){
                    console.log(data);
                    changeHtml(data["Error"], "login_mail_error");
                }else if(res.status===400){
                    changeHtml(data["Error"], "wrong_error");
                }
            });
        })
        .catch((err) => {
            console.log("Eror", err);
        });
}
function changeHtml(text, parentId) {
    parentElem = document.getElementById(parentId);
    if (typeof text != 'undefined'){
        parentElem.innerText = text
    }else {
        parentElem.innerText = ''
    }

}

function makeElement(id, name, parentId, elementType, template) {
    elem = document.createElement(elementType);
    elem.innerHTML = `id: ${id} <br /> repo-name: ${name} <br /> <br />`
    elem.setAttribute('data-id', id);
    parentElem = document.getElementById(parentId);
    console.log(parent);
    parentElem.append(elem);
}