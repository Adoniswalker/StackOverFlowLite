//This file will be used to manipulate questions
"use strict"; //enable strict mode for debugging

document.addEventListener('DOMContentLoaded', get_all_questions(), true);
const question_list_Div = document.getElementById("question_list_id");
if (form) {
    form.addEventListener("submit", create_user);
}
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
function addQuestion() {
    //To allow manipulations of this tags
    let question_subject_tag = document.forms["post_question"]["subject"];
    let question_body_tag = document.forms["post_question"]["content_question"];

    let question_subject = trimfield(question_subject_tag.value);
    let question_body = trimfield(question_body_tag.value);
    console.log(question_subject.length);
    if (! (question_subject.length<=2000 && question_subject.length>=5)) {
        changeHtml("Kindly provide a subject between 5 and 2000 characters!", "subject_error");
        question_subject_tag.focus();
        return false;
    }
    if (! (question_body.length<=2000 && question_body.length>=5)) {
        changeHtml("Kindly provide a body between 5 and 2000 characters!", "body_error");
        question_body_tag.focus();
        return false;
    } else {
        let content = (" <a href=\"UI/question_detail.html\" class=\"question_link\">\n" +
            "\n" +
            "            <div class=\"question_item\">\n" +
            "                <h4>" + row_question.value + "</h4>\n" +
            "                <p>" + row_message.value + "</p>\n" +
            "            </div>\n" +
            "        </a>");
        question_list_Div.insertAdjacentHTML('beforeend', content)
    }

}