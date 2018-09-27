let signup_form = document.getElementById('signup');

if (signup_form) {
    signup_form.addEventListener("submit", () => {
        let signup_data = new FormData(signup_form);
        create_user(signup_data);
    });
}

function create_user(signup_data) {
    fetch("/api/v1/auth/signup/", {
        method: "POST",
        mode: "cors",
        body: signup_data
    }).then((res) => {
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
    }).catch((err) => {
        console.log("Eror", err);
    });
}

const login_form = document.getElementById('login');

if (login_form) {
    login_form.addEventListener("submit", () => {
        let login_data = new FormData(login_form);
        loginUser(login_data);
    });
}

function loginUser(login_data) {
    "use strict";
    fetch("/api/v1/auth/login/", {
        method: "POST",
        mode: "cors",
        body: login_data,
        // headers: {
        //     "Content-type": "application/json; charset=UTF-8",
        // },
    }).then((res) => {
        res.json().then((data) => {
            if (res.status === 200) {
                createCookie("token", data["auth_token"], 3);
                delete data["auth_token"];
                window.localStorage.setItem('user', JSON.stringify(data));
                window.location.replace("/");
            }
            else if (res.status === 404) {
                changeHtml(data["Error"], "login_mail_error");
            } else if (res.status === 400) {
                changeHtml(data["Error"], "wrong_error");
            }
        });
    })
        .catch((err) => {
            console.log("Error", err);
        });
}

let user_question_list_Div = document.getElementById("question_questions_list");

function get_all_user_questions() {
    fetch("/api/v1/questions/user/", {
        method: "GET",
        mode: "cors",
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "Authorization": "Bearer " + read_cookie("token")
        },
    }).then((res) => {
        res.json().then((data) => {
            if (res.status === 200) {
                for (let i = 0; i < data.length; i++) {
                    insert_question_list(data[i]);
                }

            } else if (res.status === 400) {
                show_notification(data["message"]["Authorization"]);
            } else if (res.status === 404) {
                show_notification("No questions found");
            }

        });
    }).catch((err) => {
        show_notification("Unable to load questions, try again later");
    });
}

function insert_question_list(data) {
    let user = get_user();
    if (is_user_logged_in()) {
        if (user["account_id"] === data["posted_by"]) {
            data["delete_span"] = "edit";
        }
    }
    data["human_date"] = prettyDate(data["date_posted"]) || data["date_posted"];
    let temp = document.getElementById("user_questions_template");
    let content = Mustache.render(temp.innerHTML, data);
    user_question_list_Div.insertAdjacentHTML('afterbegin', content);
}

document.addEventListener('DOMContentLoaded', get_all_user_questions, true);
