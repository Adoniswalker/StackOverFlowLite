from flask import jsonify, request

from app import app

from app.questions import Questions

questions_object = Questions()


@app.route('/api/v1/questions/', methods=['get'])
def get_all_questions():
    return jsonify(questions_object.get_all_questions())

