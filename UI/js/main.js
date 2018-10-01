// theDiv.appendChild(content);
function trimfield(str) {
    return str.replace(/^\s+|\s+$/g, '');
}

function addQuestion() {
    let question_list_Div = document.getElementById("question_list_id");
    let row_question = document.forms["post_question"]["subject"];
    let row_message = document.forms["post_question"]["content_question"];
    if (trimfield(row_question.value) === '') {
        alert("Please Provide the subject of the question!");
        row_question.focus();
        return false;
    } else if (trimfield(row_message.value) === '') {
        alert("Please Provide an an explanation for your question!");
        row_message.focus();
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

function addAnswer() {
    let answersDiv = document.getElementById("answers_id");
    let row_answer = document.forms["post_answer"]["answer"];
    if (trimfield(row_answer.value) === '') {
        alert("Please Provide an answer!");
        row_answer.focus();
        return false;
    }
    else {
        let element_answer = '<div class="answer">' + row_answer.value + '</div>';
        answersDiv.insertAdjacentHTML('beforeend', element_answer);
    }

}
