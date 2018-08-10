// theDiv.appendChild(content);

function addQuestion() {
    let question_list_Div = document.getElementById("question_list_id");
    let row_question = document.forms["post_question"]["subject"].value;
    let row_message = document.forms["post_question"]["content_question"].value;
    let content = (" <a href=\"UI/question_detail.html\" class=\"question_link\">\n" +
        "\n" +
        "            <div class=\"question_item\">\n" +
        "                <h4>"+row_question+"</h4>\n" +
        "                <p>"+row_message+"</p>\n" +
        "            </div>\n" +
        "        </a>");
    question_list_Div.insertAdjacentHTML('beforeend', content)

}

function addAnswer() {
    let answersDiv = document.getElementById("answers_id");
    let row_answer = document.forms["post_answer"]["answer"].value;
    let element_answer = '<div class="answer">' + row_answer + '</div>'
    answersDiv.insertAdjacentHTML('beforeend', element_answer)

}