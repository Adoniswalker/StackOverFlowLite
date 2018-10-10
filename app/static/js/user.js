let signup_form = document.getElementById("signup");

if (signup_form) {
	signup_form.addEventListener("submit", () => {
		let signup_data = new FormData(signup_form);
		create_user(signup_data);
	});
}

const  create_user = signup_data => {
	fetch("/api/v1/auth/signup/", {
		method: "POST",
		mode: "cors",
		body: signup_data
	}).then((res) => {
		res.json().then((data) => {
			if (res.status === 201) {
				window.location.replace("/login");
			}
			else {
				changeHtml(data["message"]["email"], "email_error");
				changeHtml(data["message"]["password"], "password_error");
			}
		});
	}).catch((err) => {
	});
};

const login_form = document.getElementById("login");

if (login_form) {
	login_form.addEventListener("submit", () => {
		let login_data = new FormData(login_form);
		loginUser(login_data);
	});
}

const loginUser = login_data => {
	"use strict";
	fetch("/api/v1/auth/login/", {
		method: "POST",
		mode: "cors",
		body: login_data,
		// headers: {
		//     "Content-type": "application/json; charset=UTF-8",
		// },
	}).then((res) => {
		res.json().then((data) => {
			if (res.status === 200) {
				createCookie("token", data["auth_token"], 3);
				delete data["auth_token"];
				window.localStorage.setItem("user", JSON.stringify(data));
				window.location.replace("/");
			}
			else if (res.status === 404) {
				changeHtml(data["Error"], "login_mail_error");
			} else if (res.status === 400) {
				changeHtml(data["Error"], "wrong_error");
			}
		});
	})
		.catch((err) => {
		});
};
