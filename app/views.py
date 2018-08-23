"""This file serves the endpoints"""
import re

from flask import jsonify, request
from flask_bcrypt import Bcrypt, check_password_hash
from flask_restful import Api, Resource, reqparse

from app import app, db

from app.questions import Questions

QUESTION_OBJECT = Questions()

api = Api(app)
b_crypt = Bcrypt(app)


class QuestionsApi(Resource):
    def get(self):
        """
            This endponint will get all the questions
            :return:
            """
        return jsonify(QUESTION_OBJECT.get_all_questions())

    def post(self):
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


class QuestionGetUpdateDelete(Resource):
    def get(self, question_id):
        """
            This endpoint will fetch one question
            :rtype: jsonify
            """
        question = QUESTION_OBJECT.get_one_question(question_id)
        if not question:
            return jsonify({"Error": "Question not found"}), 404
        return jsonify(question[0])

    def delete(self, question_id):
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

    def put(self, question_id):
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


def email_address(value, name):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_regex, value.strip()):
        raise ValueError("The parameter '{}' is not a valid email. You gave us the value:{}".format(name, value))
    email_count = db.qry("select email from users where email = '{}'".format(value.strip()), fetch="rowcount")
    # import pdb; pdb.set_trace()
    if email_count >= 1:
        raise ValueError("'{}' has already been registered".format(value.strip()))
    return value


def password_valid(value, name):
    password_regex = r"(?=.{8,})"
    if not re.match(password_regex, value.strip()):
        raise ValueError(
            "The parameter '{}' must be 8 characters or more. You gave us the value:{}".format(name, value))
    return value


REGISTER_PARSER = reqparse.RequestParser(bundle_errors=True)
REGISTER_PARSER.add_argument('first_name')
REGISTER_PARSER.add_argument('last_name')
REGISTER_PARSER.add_argument('email', required=True, type=email_address)
REGISTER_PARSER.add_argument('password', required=True, type=password_valid)


class RegisterUser(Resource):
    def post(self):
        args = REGISTER_PARSER.parse_args()
        query = "insert into users (first_name, last_name, email, password_hash)" \
                " values (%s,%s,%s, %s) returning account_id, first_name, last_name,  email"
        arguments = (
            args['first_name'], args['last_name'], args['email'],
            b_crypt.generate_password_hash(args['password']).decode('utf-8'))
        results = db.qry(query, arguments, fetch="all", commit=True)
        print(results)
        return results, 201


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


LOGIN_PARSER = reqparse.RequestParser(bundle_errors=True)
LOGIN_PARSER.add_argument('email', required=True)
LOGIN_PARSER.add_argument('password', required=True)


class LoginUser(Resource):
    def post(self):
        args = LOGIN_PARSER.parse_args()
        query = "select account_id, first_name, last_name, email, password_hash from users where  email = '{}';".format(
            args['email'])
        results = db.qry(query, fetch="one")
        # import pdb; pdb.set_trace()
        if not results:
            return {"Error": "Email not registred"}
        elif check_password_hash(results['password_hash'], args['password']):
            results.pop("password_hash")
            return results, 201
        else:
            return {"Error": "Wrong password"}


api.add_resource(QuestionsApi, '/api/v1/questions/')
api.add_resource(QuestionGetUpdateDelete, '/api/v1/questions/<int:question_id>/')
api.add_resource(RegisterUser, '/api/v1/auth/user/')
api.add_resource(LoginUser, '/api/v1/auth/login/')
if __name__ == '__main__':
    app.run(debug=True)
