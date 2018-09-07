//This file will be used to manipulate questions
"use strict"; //enable strict mode for debugging

document.addEventListener('DOMContentLoaded', get_question_detail, true);
const question_body = document.getElementById("question");
const answer_body = document.getElementById("answers_id");

function get_question_detail() {
    fetch("/api/v1/questions/1/", {
        method: "GET",
        mode: "cors",
    }).then((res) => {
        res.json().then((data) => {
            if (res.status === 200) {
                console.log(data);
                let question = "<div class=\"question_detail\">" +
                    "<h3>" + data["question_subject"] + "</h3>" +
                    "<p> " + data["question_body"] + "</p>" +
                    "</div>";
                question_body.insertAdjacentHTML('afterbegin', question);
                if ((data["answers"] !== "undefined") && data["answers"].length) {
                    for (let i = 0; i < data["answers"].length; i++) {
                        insert_answer(data["answers"][i]);
                    }
                } else {
                    console.log("No answers found")
                }
            } else if (res.status === 404) {
                console.log("No questions found!!")
            }

        });
    }).catch((err) => {
        console.log("Error", err);
    });
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