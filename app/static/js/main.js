// theDiv.appendChild(content);
const trimfield = str => {
	//Remove spaces from strings
	return str.replace(/^\s+|\s+$/g, "");
};

const show_notification = (text, success) => {
	if (success) {
		$("#message").css("background-color", "green");
	} else {
		$("#message").css("background-color", "red");
	}
	$("#message span").text(text);
	$("#message").fadeIn("slow");
	$("#message a.close-notify").click(function () {
		$("#message").fadeOut("slow");
		return false;
	}
	);
};

const read_cookie = name => {
	let nameEQ = name + "=";
	let ca = document.cookie.split(";");
	for (let i = 0; i < ca.length; i++) {
		let c = ca[i];
		while (c.charAt(0) === " ") c = c.substring(1, c.length);
		if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
	}
	return null;
};

const changeHtml = (text, parentId) => {
	let parentElem = document.getElementById(parentId);
	if ((typeof text !== "undefined") && text) {
		parentElem.innerText = text;
	} else {
		parentElem.innerText = "";
	}

};

const get_user = () => {
	return JSON.parse(localStorage.getItem("user"));
};

const is_user_logged_in = ()=> {
	if (read_cookie("token")) {
		return true;
	} else {
		localStorage.removeItem("user");
		return false;
	}
};

const set_unset_user =()=> {
	if (is_user_logged_in()) {
		$("#logout_link").show().click(logout_user);
		$("#signup_link").hide();
		$("#login_link").hide();
	} else {
		$("#logout_link").hide();
		$("#signup_link").show();
		$("#login_link").show();
	}
};

const logout_user = (event) => {
	//used to logout user
	// should be here to ensure user can logout anywhere
	event.preventDefault();
	fetch("/api/v1/auth/logout/", {
		method: "POST",
		mode: "cors",
		headers: {
			"Authorization": "Bearer " + read_cookie("token")
		},
	}).then((res) => {
		res.json().then((data) => {
			if (res.status === 200) {
				//delete the token by setting past date
				let now = new Date();
				now.setMonth(now.getMonth() - 1);
				let token = "token=" + read_cookie("token");
				document.cookie = token + ";expires=" + now.toUTCString() + ";";
				// delete user details from local storage
				window.localStorage.removeItem("user");
				//redirect user to homepage
				window.location.replace("/");
			} else if (res.status === 400) {
				window.localStorage.removeItem("user");
				window.location.replace("/");
				show_notification(data["message"]["Authorization"]);
			}
		});
	})
		.catch((err) => {
		});
};

const createCookie = (name, value, days) => {
	let expires;
	if (days) {
		const date = new Date();
		date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
		expires = "; expires=" + date.toGMTString();
	}
	else {
		expires = "";
	}
	let cookie = name + "=" + value + expires;
	document.cookie = cookie;
	return cookie;
};

set_unset_user();


const popup = (parent, message) => {
	// It gives a small popup showing a message, parent is the tag to be displayed below
	//and message is the message to be passes
	if ((typeof message !== "undefined") && message) {
		$(".error-notification").remove();
		let $err = $("<div>").addClass("error-notification")
			.html("<h2>" + message + "</h2>(click on this box to close)")
			.css("left", $(parent).position().left);
		$(parent).after($err);
		$err.fadeIn("fast");
	}
};

$(document).on("click", ".error-notification", function () {
	$(this).fadeOut("fast", function () {
		$(this).remove();
	});
});

const prettyDate = (time, now = new Date()) => {
	let date = new Date(time || ""),
		diff = ((new Date(now).getTime() - date.getTime()) / 1000),
		day_diff = Math.floor(diff / 86400);

	if (isNaN(day_diff) || day_diff < 0) {
		return;
	}

	return day_diff === 0 && (diff < 60 && "just now" ||
        diff < 120 && "1 minute ago" ||
        diff < 3600 && Math.floor(diff / 60) + " minutes ago" ||
        diff < 7200 && "an hour ago" ||
        diff < 86400 && Math.floor(diff / 3600) + " hours ago") ||
        day_diff === 1 && "Yesterday" ||
        day_diff < 7 && day_diff + " days ago" ||
        day_diff < 14 && "last week" ||
        day_diff < 31 && Math.ceil(day_diff / 7) + " weeks ago" ||
        day_diff < 32 && "last month" ||
        day_diff < 366 && Math.ceil(day_diff / 30) + " months ago" ||
        day_diff < 731 && "last year" ||
        day_diff > 731 && Math.ceil(day_diff / 365) + " years ago";
};


const slide_notify =  (message) => {
	$(".custom-notification-content").html(message);
	$(".custom-social-proof").stop().slideToggle("slow");
	setTimeout(()=> {$(".custom-social-proof").stop().slideToggle("slow");}, 4000);
	$(".custom-close").click(function () {
		$(".custom-social-proof").stop().slideToggle("slow");
	});
};


const Confirm = (title, msg, $true, $false, $callback, args) => { /*change*/
	let $content =  `
    <div class='dialog-ovelay'>
        <div class='dialog'>
            <header>
                <h3> ${title} </h3> 
                <i class='fa fa-close'></i>
            </header>
        <div class='dialog-msg'>
            <p> ${msg} </p> 
        </div>
        <footer>
            <div class='controls'>
                <button class='button button-danger doAction'>${$true}</button> 
                <button class='button button-default cancelAction'>${$false}</button>
            </div>
        </footer>
     </div>`;
	$("body").prepend($content);
	$(".doAction").click(function () {
		$callback.apply(false, args);
		$(this).parents(".dialog-ovelay").fadeOut(500, function () {
			$(this).remove();
		});
		return true;
	});
	$(".cancelAction, .fa-close").click(function () {
		$(this).parents(".dialog-ovelay").fadeOut(500, function () {
			$(this).remove();
		});
	});

};
