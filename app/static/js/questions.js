//This file will be used to manipulate questions
"use strict"; //enable strict mode for debugging


class Questions {
    constructor() {
        this.question_list_Div = document.getElementById("question_list_id");
    }

    get_all_questions() {
        fetch("/api/v1/questions/", {
            method: "GET",
            mode: "cors",
        }).then((res) => {
            res.json().then((data) => {
                if (res.status === 200) {
                    for (let i = 0; i < data.length; i++) {
                        this.insert_question_list(data[i]);
                    }

                } else if (res.status === 404) {
                    show_notification("No questions found");
                }

            });
        }).catch(() => {
            show_notification("Unable to load questions, try again later");
        });
    };

    addQuestion() {
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
            this.postQuestion(data, question_subject_tag, question_body_tag)
        }
    }

    postQuestion(data, question_subject_tag, question_body_tag) {
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
                    this.insert_question_list(data);
                    question_subject_tag.value = '';
                    question_body_tag.value = '';
                    slide_notify("<p>You successfully posted the question<small>Just now</small></p>");
                }
                else if (res.status === 400) {
                    changeHtml(data["message"]["Authorization"], "login_error");
                    changeHtml(data["message"]["question_subject"], "subject_error");
                    changeHtml(data["message"]["question_body"], "body_error");
                } else {
                    popup("#login_error", data["message"]["Authorization"]);
                }
            });
        }).catch(() => {
            show_notification("Unable to connect to the internet");
        });
    }

    insert_question_list(data) {
        // This function will inset posted questions to a list
        let user = get_user();
        let is_user_logged = is_user_logged_in();
        if (is_user_logged) {
            if (user["account_id"] === data["posted_by"]) {
                data["delete_span"] = "edit";
            }
        }
        data["human_date"] = prettyDate(data["date_posted"]) || Questions.readable_date(data["date_posted"]);
        data["date_posted"] = Questions.readable_date(data["date_posted"]);
        let temp = document.getElementById("questions_template");
        let content = Mustache.render(temp.innerHTML, data);
        this.question_list_Div.insertAdjacentHTML('afterbegin', content);
    };

    static readable_date(comp_date) {
        let date = new Date(comp_date || "");
        return date.toLocaleString();
    };
}

const questions_object = new Questions();
document.addEventListener('DOMContentLoaded', () => {
    questions_object.get_all_questions()
}, true);

const addQuestion = () => {
    questions_object.addQuestion();
};
