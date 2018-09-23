//This file will be used to manipulate questions
"use strict"; //enable strict mode for debugging


class Questions {
    constructor() {
        this.question_body = document.getElementById("question");
        this.question_id = this.question_body.getAttribute("data-id");
        this.answer_body = document.getElementById("answers_id");
    }

    get_question_detail() {
        self = this;
        fetch(`/api/v1/questions/${this.question_id}/`, {
            method: "GET",
            mode: "cors",
        }).then((res) => {
            res.json().then((data) => {
                if (res.status === 200) {
                    let temp = document.getElementById("question_detail_template");
                    data["human_date"] = prettyDate(data["date_posted"]) || data["date_posted"];
                    let question = Mustache.render(temp.innerHTML, data);
                    this.question_body.insertAdjacentHTML('afterbegin', question);
                    this.set_delete_function(data);
                    if ((data["answers"] !== "undefined") && data["answers"].length) {
                        for (let i = 0; i < data["answers"].length; i++) {
                            self.insert_answer(data["answers"][i], this.answer_body, data["posted_by"]);
                        }
                    } else {
                        popup(".question_item", "No answers found");
                    }
                } else if (res.status === 404) {
                    show_notification("No questions found!!");
                }

            });
        }).catch((err) => {
            show_notification("Error" + err);
        });
    }

    set_delete_function(data) {
        let self = this;
        let delete_btn = this.question_body.querySelector(".delete-question");
        let edit_btn = this.question_body.querySelector(".edit-question");
        delete_btn.addEventListener("click", function () {
            self.delete_question();
        });
        edit_btn.addEventListener("click", function () {
            self.set_question();
        });
        document.getElementById('cancel_edit').addEventListener("click", function () {
            self.question_remove_edit();
        });
        document.getElementById('update_edit').addEventListener("click", function () {
            self.update_question();
        });
        let user = get_user();
        if (user) {
            if (user["account_id"] === data["posted_by"]) {
                this.question_body.classList.add("auth-priv");
            }
        }
    }

    set_question() {
        this.question_body.classList.add("main-edit");
        this.question_body.querySelector("#question_subject_edit").value = this.question_body.querySelector("h3").innerText;
        this.question_body.querySelector("#question_body_edit").value = this.question_body.querySelector("p").innerText;
    }

    question_remove_edit() {
        this.question_body.classList.remove("main-edit");
    }

    update_question() {
        let data = {
            "question_subject": this.question_body.querySelector("#question_subject_edit").value,
            "question_body": this.question_body.querySelector("#question_body_edit").value
        };
        fetch("/api/v1/questions/" + this.question_id + "/", {
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
                    this.question_body.querySelector("h3").innerText = data["question_subject"];
                    this.question_body.querySelector("p").innerText = data["question_body"];
                    this.question_remove_edit()
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
                    popup("#question_error", data["message"]["question"] + this.question_id);
                }
            });
        }).catch((err) => {
            show_notification("Error" + err);
        });
    }

    delete_question() {
        fetch("/api/v1/questions/" + this.question_body.getAttribute("data-id") + "/", {
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
                    popup("#question_error", data["message"]["question"] + this.question_id);
                }
            });
        }).catch((err) => {
            show_notification("Error" + err);
        });
    }

    addAnswer() {
        self = this;
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
            fetch(`/api/v1/questions/${this.question_id}/answers/`, {
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
                        self.insert_answer(data, this.answer_body);
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
}

class Answers extends Questions {

    static cancelAnswerEdit(answer) {
        answer.classList.remove("answer-edit");
    }

    submitEdit(answer) {
        let answer_text = answer.querySelector(".answer-edit").value;
        let answer_id = answer.getAttribute("data-id");
        fetch(`/api/v1/questions/${this.question_id}/answers/${answer_id}/`, {
            method: "PUT",
            mode: "cors",
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                "Authorization": "Bearer " + read_cookie("token"),
            },
            body: JSON.stringify({"answer": answer_text}),
        }).then((res) => {
            res.json().then((data) => {
                if (res.status === 200) {
                    show_notification("Answer successfully edited");
                    Answers.cancelAnswerEdit(answer);
                    answer.querySelector("p").innerText = data["answer"];
                }
                else if (res.status === 401) {
                    // changeHtml(data["message"]["Authorization"], "login_err");
                    popup("#answer_edit_error", data["message"]["Authorization"]);
                } else if (res.status === 403) {
                    popup("#answer_edit_error", data["message"]["Authorization"]);
                }
                else if (res.status === 404) {
                    popup("#answer_edit_error", data["message"]["question"] + this.question_id);
                }
            });
        }).catch((err) => {
            show_notification("Error" + err);
        });
    }

    insert_answer(answer, answer_body, question_ownwer) {
        self = this;
        let answer_id = answer["answer_id"];
        let temp = document.getElementById("answers_template");
        answer["human_date"] = prettyDate(answer["answer_date"]) || answer["answer_date"];
        let content = Mustache.render(temp.innerHTML, answer);
        answer_body.insertAdjacentHTML('afterbegin', content);
        let d = answer_body.querySelector(`[data-id='${answer_id}'`);

        this.set_edit_btn_answer(answer, d, question_ownwer);
        if (d) {
            d.querySelector(".click-edit-answer").addEventListener('click', function () {
                d.classList.add("answer-edit");
                d.querySelector(".answer-edit").value = d.querySelector("p").innerText;
                d.querySelector(".answer_edit").addEventListener("click", function () {
                    self.submitEdit(d);
                });
                d.querySelector(".cancel_answer_edit").addEventListener("click", function () {
                    Answers.cancelAnswerEdit(d);
                })
            })
        }
    }

    set_preferred(answer, answer_body, answer_checkbox) {
        fetch(`/api/v1/questions/${answer["question_id"]}/answers/${answer["answer_id"]}/`, {
            method: "PUT",
            mode: "cors",
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                "Authorization": "Bearer " + read_cookie("token"),
            },
            body: JSON.stringify({"vote": answer_checkbox.checked}),
        }).then((res) => {
            res.json().then((data) => {
                if (res.status === 200) {
                    if (data["accepted"]) {
                        answer_body.classList.add("accepted-display");
                        show_notification("Answer successfully accepted");
                    } else {
                        answer_body.classList.remove("accepted-display");
                        show_notification("Answer successfully unaccepted");
                    }

                }
                else if (res.status === 401) {
                    // changeHtml(data["message"]["Authorization"], "login_err");
                    popup("#answer_edit_error", data["message"]["Authorization"]);
                } else if (res.status === 403) {
                    popup("#answer_edit_error", data["message"]["Authorization"]);
                }
                else if (res.status === 404) {
                    popup("#answer_edit_error", data["message"]["question"]);
                }
            });
        }).catch((err) => {
            show_notification("Error" + err);
        });
    }

    set_edit_btn_answer(answer, answer_body, question_owner) {
        let self = this;
        let user = get_user();
        if (answer["accepted"]) {
            answer_body.classList.add("accepted-display");
        }
        if (user && (user["account_id"] === answer["answeres_by"])) {
            answer_body.classList.add("auth-answer");

        }
        if (user && (user))
            if (user && (user["account_id"] === question_owner)) {
                let answer_checkbox = answer_body.querySelector(".accept-checkbox");
                answer_body.classList.add("question_owner");
                answer_checkbox.addEventListener("change", function () {
                    self.set_preferred(answer, answer_body, answer_checkbox)
                });
                if (answer["accepted"]) {
                    answer_checkbox.checked = true;
                }
            }
        return answer
    }

}

const q = new Answers();
document.addEventListener('DOMContentLoaded', function () {
    q.get_question_detail();
}, true);

function addAnswer() {
    q.addAnswer()
}




