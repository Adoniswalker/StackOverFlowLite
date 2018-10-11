//This file will be used to manipulate questions
"use strict"; //enable strict mode for debugging


class Question {
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
					this.question_body.insertAdjacentHTML("afterbegin", question);
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
			// Confirm("Are you sure", "Are you sure you want to delete this question", "Yes", "Close", self.delete_question);
			self.delete_question();
		});
		edit_btn.addEventListener("click", function () {
			self.set_question();
		});
		document.getElementById("cancel_edit").addEventListener("click", function () {
			self.question_remove_edit();
		});
		document.getElementById("update_edit").addEventListener("click", function () {
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
					this.question_remove_edit();
					slide_notify("<p>You have successfully updated this question</p>");
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
			this.postAnswer(data, answer_tag);
		}
	}

	postAnswer(data, answer_tag){
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
                    answer_tag.value = "";
                    slide_notify("Your answer was successfully posted")
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

class Answers extends Question {

	static cancelAnswerEdit(answer) {
		answer.classList.remove("answer-edit");
	}

	submitEdit(answer) {
		let answer_text = answer.querySelector("#answer-edit").value;
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
					Answers.cancelAnswerEdit(answer);
					answer.querySelector("p").innerText = data["answer"];
                    slide_notify("Answer successfully edited");
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

	insert_answer(answer, answer_body, question_owner) {
		self = this;
		let answer_id = answer["answer_id"];
		let temp = document.getElementById("answers_template");
		answer["human_date"] = prettyDate(answer["answer_date"]) || answer["answer_date"];
		let content = Mustache.render(temp.innerHTML, answer);
		answer_body.insertAdjacentHTML("afterbegin", content);
		let answer_element = answer_body.querySelector(`[data-id='${answer_id}']`);

		this.set_edit_btn_answer(answer, answer_element, question_owner);
		if (answer_element) {
			answer_element.querySelector(".click-edit-answer").addEventListener("click", () => {
				answer_element.classList.add("answer-edit");
				answer_element.querySelector("#answer-edit").value = answer_element.querySelector("p").innerText;
				answer_element.querySelector(".answer_edit_btn").addEventListener("click", () => {
					self.submitEdit(answer_element);
				});
				answer_element.querySelector(".cancel_answer_edit").addEventListener("click", () => {
					Answers.cancelAnswerEdit(answer_element);
				});
			});
			answer_element.querySelector(".click-delete-answer").addEventListener("click", () => {
				Confirm("Delete answer", "Are you sure you want to delete answer?", "Yes", "Close",
					Answers.delete,[answer, answer_element, answer_body]);
			});
		}
	}
	static delete (answer, d, answer_body){
		fetch(`/api/v1/questions/${answer["question_id"]}/answers/${answer["answer_id"]}/`, {
			method: "DELETE",
			mode: "cors",
			headers: {
				"Content-type": "application/json; charset=UTF-8",
				"Authorization": "Bearer " + read_cookie("token"),
			}
		}).then((res) => {
			res.json().then((data) => {
				if (res.status === 200) {
					answer_body.removeChild(d);
					// dpopup("#answer_edit_error", data["message"]["answer"]);
                    slide_notify("Answer successfully deleted");
				}
				else if (res.status === 401) {
					popup("#answer_edit_error", data["message"]["Authorization"]);
				} else if (res.status === 403) {
					popup("#answer_edit_error", data["message"]["Authorization"]);
				}
				else if (res.status === 404) {
					popup("#answer_edit_error", data["message"]["answer"]);
				}
			});
		}).catch((err) => {
			show_notification("Error" + err);
		});
	}
	set_preferred(answer, answer_body) {
		// answer_body.setAttribute("waxi", "me");
		let data_accepted = answer_body.getAttribute("data-accepted");
		let accept_value = ( data_accepted !== "true");
		fetch(`/api/v1/questions/${answer["question_id"]}/answers/${answer["answer_id"]}/`, {
			method: "PUT",
			mode: "cors",
			headers: {
				"Content-type": "application/json; charset=UTF-8",
				"Authorization": "Bearer " + read_cookie("token"),
			},
			body: JSON.stringify({"vote": accept_value}),
		}).then((res) => {
			res.json().then((data) => {
				if (res.ok) {
					if(data["accepted"]){
						answer_body.querySelector(".accept-icon").src = "/static/images/dislike.png";
						answer_body.setAttribute("data-accepted", "true");
						answer_body.classList.add("accepted-display");
					}else {
						answer_body.setAttribute("data-accepted", "false");
						answer_body.querySelector(".accept-icon").src = "/static/images/like.png";
						answer_body.classList.remove("accepted-display");
					}
				}
				else{
					popup("#answer_edit_error", data["message"]["Authorization"]);
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
				let accept_icon = answer_body.querySelector(".accept-icon");
				answer_body.classList.add("question_owner");
				accept_icon.addEventListener("click", function () {
					self.set_preferred(answer, answer_body, accept_icon);
				});
				if (answer["accepted"]) {
					accept_icon.checked = true;
				}
			}
		return answer;
	}

}

const answer_obj = new Answers();
document.addEventListener("DOMContentLoaded", function () {
	answer_obj.get_question_detail();
}, true);

const  addAnswer = () => {
	answer_obj.addAnswer();
};
