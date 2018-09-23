// theDiv.appendChild(content);
function trimfield(str) {
    //Remove spaces from strings
    return str.replace(/^\s+|\s+$/g, '');
}

function show_notification(text, success) {
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
    });
}

function read_cookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function changeHtml(text, parentId) {
    let parentElem = document.getElementById(parentId);
    if ((typeof text !== 'undefined') && text) {
        parentElem.innerText = text
    } else {
        parentElem.innerText = ''
    }

}

function get_user() {
    return JSON.parse(localStorage.getItem('user'));
}

function set_unset_user() {
    if (get_user()) {
        $("#logout_link").show().click(logout_user);
        $("#signup_link").hide();
        $("#login_link").hide();
    } else {
        $("#logout_link").hide();
        $("#signup_link").show();
        $("#login_link").show();
    }
}

function logout_user(event) {
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
                console.log(data);

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
                // changeHtml(data["Error"], "wrong_error");
                // changeHtml(data["message"]["email"], "login_mail_error");
            }
        });
    })
        .catch((err) => {
            console.log("Eror", err);
        });
}

function createCookie(name, value, days) {
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
}

set_unset_user();


function popup(parent, message) {
    // It gives a small popup showing a message, parent is the tag to be displayed below
    //and message is the message to be passes
    if ((typeof message !== 'undefined') && message) {
        $('.error-notification').remove();
        let $err = $('<div>').addClass('error-notification')
            .html('<h2>' + message + '</h2>(click on this box to close)')
            .css('left', $(parent).position().left);
        $(parent).after($err);
        $err.fadeIn('fast');
    }
}

$(document).on('click', ".error-notification", function () {
    $(this).fadeOut('fast', function () {
        $(this).remove();
    });
});

function prettyDate(time, now = new Date()) {
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
}
