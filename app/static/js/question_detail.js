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
                console.log(data);
                let question = "<div class=\"question_detail\">" +
                    "<h3>" + data["question_subject"] + "</h3>" +
                    "<span class=\"question_vote\">5</span><span class=\"votes\">Answers</span>" +
                    "<p> " + data["question_body"] + "</p>" +
                    "<span class=\"question_tip\">Asked at " + data["date_posted"] + " by " +
                    data["posted_by"] + " </span>" +
                    "</div>";
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
    let answersDiv = document.getElementById("answers_id");
    let answer_tag = document.forms["post_answer"]["answer"];
    let answer = trimfield(answer_tag.value);
    if (!(answer.length <= 2000 && answer.length >= 5)) {
        changeHtml("Kindly provide an answer between 5 and 2000 characters!", "answer_error");
        answer_tag.focus();
        return false;
    } else {
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
                    changeHtml(data["message"]["Authorization"], "login_err");
                    changeHtml(data["message"]["answer"], "answer_error");
                } else if (res.status === 404) {
                    changeHtml(data["message"]["question"], "login_err");
                }
            });
        }).catch((err) => {
            show_notification("Error" + err);
        });
    }

}

function insert_answer(answer) {
    let accepted = answer["accepted"] ? "Accepted" : '';
    let content = "<div class=\"answer\" data-id=" + answer["answer_id"] + ">" +
        answer["answer"] +
        "<span class=\"question_tip\">Answered at " + answer["answer_date"] + " by " + answer["answeres_by"] + " </span>" +
        "<p class=\"success\">" + accepted + "</p>" +
        "</div>";
    answer_body.insertAdjacentHTML('afterbegin', content)
}