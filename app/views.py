"""This file serves the endpoints"""
from flask import jsonify, request

from app import app

from app.questions import Questions

QUESTION_OBJECT = Questions()


@app.route('/api/v1/questions/', methods=['get'])
def get_all_questions():
    """
    This endponint will get all the questions
    :return:
    """
    return jsonify(QUESTION_OBJECT.get_all_questions())


@app.route('/api/v1/questions/<int:question_id>/', methods=['get'])
def fetch_question(question_id):
    """
    This endpoint will fetch one question
    :rtype: jsonify
    """
    question = QUESTION_OBJECT.get_one_question(question_id)
    if not question:
        return jsonify({"Error": "Question not found"}), 404
    return jsonify(question[0])


@app.route('/api/v1/questions/', methods=['post'])
def post_question():
    """
    Thois endpoint will post a new answer
    :rtype: object
    """
    subject = request.json.get('subject') or ''
    body = request.json.get('body') or ''
    if not all([body, subject]):
        return jsonify({"Error": "Please provide all fields with keys 'subject' and 'body'"}), 400
    question_dict = QUESTION_OBJECT.post_question(subject, body)
    return jsonify(question_dict), 201


@app.route('/api/v1/questions/<int:question_id>/answers/', methods=['post'])
def post_answer(question_id):
    """
    This function will post a new answer
    :rtype: object
    """
    answer = request.json.get('answer') or ''
    if not answer:
        return jsonify({"Error": "Kindly provide an answer with data and with field 'answer'"}), 400
    answer_result = QUESTION_OBJECT.post_answer(question_id, answer)
    if not answer_result:
        return jsonify({"Error": "No question found"}), 404
    return jsonify({'question_id': question_id, 'answer': answer}), 201


@app.route('/api/v1/questions/<int:question_id>/', methods=['delete'])
def delete_question(question_id):
    """
    This function will delete a question
    :param question_id:
    :return:
    """
    question_result = QUESTION_OBJECT.delete_question(question_id)
    if question_result:
        return jsonify({"Success": "Question deleted"}), 204
    else:
        return jsonify({"Error": "Question not found"}), 404


@app.route('/api/v1/questions/<int:question_id>/', methods=['put'])
def update_question(question_id: int) -> object:
    """
    This endpont will update subject and body when called
    :param question_id:
    :return:
    """
    subject = request.json.get('subject') or ''
    body = request.json.get('body') or ''
    if not all([body, subject]):
        return jsonify({"Error": "Please provide all fields with keys 'subject' and 'body'"}), 400
    question_response = QUESTION_OBJECT.update_question(question_id, subject, body)
    if not question_response:
        return jsonify({"Error": "No question found"}), 404
    return jsonify(question_response), 200
