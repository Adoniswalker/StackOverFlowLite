//This file will be used to manipulate questions
"use strict"; //enable strict mode for debugging

document.addEventListener('DOMContentLoaded', get_question_detail, true);
const question_body = document.getElementById("question");
const answer_body = document.getElementById("answers_id");
let question_id = question_body.getAttribute("data-id");

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
                }
                else if (res.status === 400) {
                    // changeHtml(data["message"]["Authorization"], "login_err");
                    popup("#login_err", data["message"]["Authorization"]);
                    changeHtml(data["message"]["answer"], "answer_error");
                } else if (res.status === 404) {
                    changeHtml(data["message"]["question"], "login_err");
                }
                else  if (res.status === 403){
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
    let content= Mustache.render(temp.innerHTML, answer);
    answer_body.insertAdjacentHTML('afterbegin', content)
}