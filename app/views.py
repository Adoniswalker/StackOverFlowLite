from flask import jsonify, request

from app import app

from app.questions import Questions

questions_object = Questions()


@app.route('/api/v1/questions/', methods=['get'])
def get_all_questions():
    return jsonify(questions_object.get_all_questions())


@app.route('/api/v1/questions/<int:questionId>/', methods=['get'])
def fetch_question(questionId):
    question = questions_object.get_one_question(questionId)
    if not question:
        return jsonify({"Error": "Question not found"}), 404
    return jsonify(question)


@app.route('/api/v1/questions/', methods=['post'])
def post_question():
    subject = request.json.get('subject') or ''
    body = request.json.get('body') or ''
    if not all([body, subject]):
        return jsonify({"Error": "Please provide all fields with keys 'subject' and 'body'"}), 400
    question_dict = questions_object.post_question(subject, body)
    return jsonify(question_dict), 201


@app.route('/api/v1/questions/<int:questionId>/answers/', methods=['post'])
def post_answer(questionId):
    answer = request.json.get('answer') or ''
    if not answer:
        return jsonify({"Error": "Kindly provide an answer with data and with field 'answer'"}), 400
    answer_result = questions_object.post_answer(questionId, answer)
    if not answer_result:
        return jsonify({"Error": "No question found"}), 404
    return jsonify({'question_id': questionId, 'answer': answer}), 201
