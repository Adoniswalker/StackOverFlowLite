// theDiv.appendChild(content);
function trimfield(str) {
    //Remove spaces from strings
    return str.replace(/^\s+|\s+$/g, '');
}

function show_notification(text) {
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
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function changeHtml(text, parentId) {
    parentElem = document.getElementById(parentId);
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

function check_user_loggedin() {
    if (read_cookie("token")) {
        return true;
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

                //delete the token by setting letter date
                let now = new Date();
                now.setMonth(now.getMonth() - 1);
                document.cookie = "token=" + read_cookie("token");
                document.cookie = "expires = " + now.toUTCString() + ";";

                // delete user details from local storage
                window.localStorage.removeItem("user");
                //redirect user to homepage
                window.location.replace("/");
            } else if (res.status === 400) {
                window.localStorage.removeItem("user");
                show_notification(data["Error"])
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
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        var expires = "; expires=" + date.toGMTString();
    }
    else var expires = "";
    // document.cookie = name + "=" + value + expires + "; path=/";
    document.cookie = name + "=" + value + expires + ";";
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
