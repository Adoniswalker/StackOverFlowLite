// theDiv.appendChild(content);
function trimfield(str) {
    //Remove spaces from strings
    return str.replace(/^\s+|\s+$/g, '');
}

function addAnswer() {
    let answersDiv = document.getElementById("answers_id");
    let row_answer = document.forms["post_answer"]["answer"];
    if (trimfield(row_answer.value) == '') {
        alert("Please Provide an answer!");
        row_answer.focus();
        return false;
    }
    else {
        let element_answer = '<div class="answer">' + row_answer.value + '</div>';
        answersDiv.insertAdjacentHTML('beforeend', element_answer);
    }

}

