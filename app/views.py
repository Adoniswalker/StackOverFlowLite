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
