//This file will be used to manipulate questions
"use strict"; //enable strict mode for debugging

document.addEventListener('DOMContentLoaded', get_all_questions(), true);
const question_list_Div = document.getElementById("question_list_id");

function get_all_questions() {
    fetch("/api/v1/questions/", {
        method: "GET",
        mode: "cors",
    }).then((res) => {
        res.json().then((data) => {
            if (res.status === 200) {
                for (let i = 0; i < data.length; i++) {
                    insert_question_list(data[i]);
                }

            } else if (res.status === 404) {
                show_notification("No questions found");
            }

        });
    }).catch((err) => {
        show_notification("Unable to load questions, try again later");
    });
}

function addQuestion() {
    //To allow manipulations of this tags
    let question_subject_tag = document.forms["post_question"]["subject"];
    let question_body_tag = document.forms["post_question"]["content_question"];

    let question_subject = trimfield(question_subject_tag.value);
    let question_body = trimfield(question_body_tag.value);
    if (!(question_subject.length <= 2000 && question_subject.length >= 5)) {
        changeHtml("Kindly provide a subject between 5 and 2000 characters!", "subject_error");
        question_subject_tag.focus();
        return false;
    }
    if (!(question_body.length <= 2000 && question_body.length >= 5)) {
        changeHtml("Kindly provide a body between 5 and 2000 characters!", "body_error");
        question_body_tag.focus();
        return false;
    } else {
        //Clear errors on form if any
        changeHtml(false, "subject_error");
        changeHtml(false, "body_error");
        let data = {
            "question_subject": question_subject,
            "question_body": question_body
        };
        fetch("/api/v1/questions/", {
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
                    insert_question_list(data);
                    question_subject_tag.value = '';
                    question_body_tag.value = '';
                }
                else if (res.status === 400) {
                    changeHtml(data["message"]["Authorization"], "login_error");
                    changeHtml(data["message"]["question_subject"], "subject_error");
                    changeHtml(data["message"]["question_body"], "body_error");
                } else {
                    popup("#login_error", data["message"]["Authorization"]);
                }
            });
        }).catch((err) => {
            show_notification("Error: " + err);
        });
    }

}

function insert_question_list(data) {
    // This function will inset posted questions to a list
    let user = get_user();
    if (user) {
        if (user.account_id === data.posted_by) {
            data["delete_span"] = "edit";
        }
    }
    data["human_date"] = prettyDate(data["date_posted"]) || data["date_posted"];
    let temp = document.getElementById("questions_template");
    let content = Mustache.render(temp.innerHTML, data);
    question_list_Div.insertAdjacentHTML('afterbegin', content);
}