//This file will be used to manipulate questions
"use strict"; //enable strict mode for debugging

document.addEventListener('DOMContentLoaded', get_all_questions(), true);
var question_list_Div = document.getElementById("question_list_id");

function get_all_questions() {
    fetch("/api/v1/questions/", {
        method: "GET",
        mode: "cors",
    }).then((res) => {
        res.json().then((data) => {
            if (res.status === 200) {
                console.log(data);
                for (var i = 0; i < data.length; i++) {
                    let content = (" <a href=\"UI/question_detail.html\" class=\"question_link\">\n" +
                        "\n" +
                        "            <div class=\"question_item\" data-id=" + data[i]["question_id"] + ">\n" +
                        "                <h4>" + data[i]["question_subject"] + "</h4>\n" +
                        "<span class=\"question_vote\">5</span><span class=\"votes\">Answers</span>" +
                        "                <p>" + data[i]["question_body"] + "</p>\n" +
                        "<span class=\"question_tip\">Asked at " + data[i]["date_posted"] + " by "+ data[i]["posted_by"] + " </span>" +
                        "            </div>\n" +
                        "        </a>");
                    question_list_Div.insertAdjacentHTML('afterbegin', content)
                }

            } else if (res.status === 404) {
                console.log("No questions found!!")
            }

        });
    }).catch((err) => {
        console.log("Error", err);
    });
}