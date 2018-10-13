import Mustache from 'mustache'
import {show_notification,read_cookie,get_user, is_user_logged_in, prettyDate} from './main'
const get_all_user_questions = ()=> {
	fetch("/api/v1/questions/user/", {
		method: "GET",
		mode: "cors",
		headers: {
			"Content-type": "application/json; charset=UTF-8",
			"Authorization": "Bearer " + read_cookie("token")
		},
	}).then((res) => {
		res.json().then((data) => {
			if (res.status === 200) {
				set_counts();
				for (let i = 0; i < data.length; i++) {
					insert_question_list(data[i]);
				}

			} else if (res.status === 400) {
				show_notification(data["message"]["Authorization"]);
			} else if (res.status === 404) {
				show_notification("No questions found");
			}

		});
	}).catch((err) => {
		show_notification("Unable to load questions, try again later");
	});
};

document.addEventListener("DOMContentLoaded", get_all_user_questions, true);

const set_counts = ()=> {
	let question_count = document.getElementById("question_count");
	let answer_count = document.getElementById("answer_count");
	fetch("/api/v1/auth/signup/", {
		method: "GET",
		mode:"cors",
		headers:{
			"Content-type":"application/json; charset=UTF-8",
			"Authorization":"Bearer "+ read_cookie("token")
		},
	}).then((res)=>{
		res.json().then((data)=>{
			if(res.status === 200){
				question_count.innerText=data["questions_counts"];
				answer_count.innerText=data["answers_counts"];
			}
		});
	});
};
const insert_question_list = (data) => {
	let user_question_list_Div = document.getElementById("question_questions_list");
	let user = get_user();
	if (is_user_logged_in()) {
		if (user["account_id"] === data["posted_by"]) {
			data["delete_span"] = "edit";
		}
	}
	data["human_date"] = prettyDate(data["date_posted"]) || data["date_posted"];
	let temp = document.getElementById("user_questions_template");
	let content = Mustache.render(temp.innerHTML, data);
	user_question_list_Div.insertAdjacentHTML("afterbegin", content);
};
