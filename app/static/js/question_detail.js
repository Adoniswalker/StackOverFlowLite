//This file will be used to manipulate questions
"use strict"; //enable strict mode for debugging

document.addEventListener('DOMContentLoaded', get_question_detail, true);
const question_body = document.getElementById("question");
const answer_body = document.getElementById("answers_id");
let question_id = question_body.getAttribute("data-id");


function set_question() {
    question_body.classList.add("main-edit");
    question_body.querySelector("#question_subject_edit").value = question_body.querySelector("h3").innerText;
    question_body.querySelector("#question_body_edit").value = question_body.querySelector("p").innerText;
}

function remove_edit() {
    question_body.classList.remove("main-edit");
}

function update_question() {
    let data = {
        "question_subject": question_body.querySelector("#question_subject_edit").value,
        "question_body": question_body.querySelector("#question_body_edit").value
    };
    fetch("/api/v1/questions/" + question_id + "/", {
        method: "PUT",
        mode: "cors",
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "Authorization": "Bearer " + read_cookie("token")
        },
        body: JSON.stringify(data)
    }).then((res) => {
        res.json().then((data) => {
            if (res.status === 200) {
                question_body.querySelector("h3").innerText = data["question_subject"];
                question_body.querySelector("p").innerText = data["question_body"];
                console.log(data);
                remove_edit()
            }
            else if (res.status === 400) {
                popup("#question_error", data["message"]["question_subject"]);
                popup("#question_error", data["message"]["question_body"]);
            }
            else if (res.status === 401) {
                popup("#question_error", data["message"]["Authorization"]);
            } else if (res.status === 403) {
                popup("#question_error", data["message"]["Authorization"]);
            }
            else if (res.status === 404) {
                popup("#question_error", data["message"]["question"] + question_id);
            }
        });
    }).catch((err) => {
        show_notification("Error" + err);
    });
}

function set_delete_function(data) {
    let delete_btn = question_body.querySelector(".delete-question");
    let edit_btn = question_body.querySelector(".edit-question");
    delete_btn.addEventListener("click", delete_question);
    edit_btn.addEventListener("click", set_question);
    document.getElementById('cancel_edit').addEventListener("click", remove_edit);
    document.getElementById('update_edit').addEventListener("click", update_question);
    let user = get_user();
    if (user) {
        if (user.account_id === data.posted_by) {
            question_body.classList.add("auth-priv");
        }
    }
}

function get_question_detail() {
    fetch("/api/v1/questions/" + question_id + "/", {
        method: "GET",
        mode: "cors",
    }).then((res) => {
        res.json().then((data) => {
            if (res.status === 200) {
                let temp = document.getElementById("question_detail_template");
                let question = Mustache.render(temp.innerHTML, data);
                question_body.insertAdjacentHTML('afterbegin', question);
                set_delete_function(data);
                if ((data["answers"] !== "undefined") && data["answers"].length) {
                    for (let i = 0; i < data["answers"].length; i++) {
                        insert_answer(data["answers"][i]);
                    }
                } else {
                    popup(".question_detail", "No answers found");
                }
            } else if (res.status === 404) {
                show_notification("No questions found!!");
            }

        });
    }).catch((err) => {
        console.log("Error", err);
        show_notification("Error" + err);
    });
}

function addAnswer() {
    let answer_tag = document.forms["post_answer"]["answer"];
    let answer = trimfield(answer_tag.value);
    if (!(answer.length <= 2000 && answer.length >= 5)) {
        changeHtml("Kindly provide an answer between 5 and 2000 characters!", "answer_error");
        answer_tag.focus();
        return false;
    } else {
        //clear any previous errors
        changeHtml(false, "answer_error");
        let data = {"answer": answer};
        fetch("/api/v1/questions/" + question_id + "/answers/", {
            method: "POST",
            mode: "cors",
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                "Authorization": "Bearer " + read_cookie("token")
            },
            body: JSON.stringify(data)
        }).then((res) => {
            res.json().then((data) => {
                if (res.status === 201) {
                    insert_answer(data);
                    answer_tag.value = ''
                }
                else if (res.status === 400) {
                    // changeHtml(data["message"]["Authorization"], "login_err");
                    popup("#login_err", data["message"]["Authorization"]);
                    changeHtml(data["message"]["answer"], "answer_error");
                } else if (res.status === 404) {
                    changeHtml(data["message"]["question"], "login_err");
                }
                else if (res.status === 403) {
                    popup("#login_err", data["message"]["Authorization"]);
                }
            });
        }).catch((err) => {
            show_notification("Error" + err);
        });
    }

}

function insert_answer(answer) {
    answer["accepted"] = answer["accepted"] ? "Accepted" : '';
    let temp = document.getElementById("answers_template");
    let content = Mustache.render(temp.innerHTML, answer);
    answer_body.insertAdjacentHTML('afterbegin', content)
}

function delete_question() {
    fetch("/api/v1/questions/" + this.getAttribute("data-id") + "/", {
        method: "DELETE",
        mode: "cors",
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "Authorization": "Bearer " + read_cookie("token")
        },
    }).then((res) => {
        res.json().then((data) => {
            if (res.status === 200) {
                show_notification("Error" + "Question successfully deleted");
                window.location.replace("/");
            }
            else if (res.status === 401) {
                // changeHtml(data["message"]["Authorization"], "login_err");
                popup("#question_error", data["message"]["Authorization"]);
            } else if (res.status === 403) {
                popup("#question_error", data["message"]["Authorization"]);
            }
            else if (res.status === 404) {
                popup("#question_error", data["message"]["question"] + question_id);
            }
        });
    }).catch((err) => {
        show_notification("Error" + err);
    });
}

