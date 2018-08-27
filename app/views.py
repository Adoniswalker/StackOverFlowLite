"""This file serves the endpoints"""
import re

from flask_bcrypt import Bcrypt, check_password_hash
from flask_restful import Api, Resource, reqparse

from app import app, db, auth
from app.answers import PostAnswer, UpdateAnswer
from app.questions import QuestionsApi, QuestionGetUpdateDelete

api = Api(app)
b_crypt = Bcrypt(app)


def email_address(value, name):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_regex, value.strip()):
        raise ValueError("The parameter '{}' is not a valid email. You gave us the value:{}".format(name, value))
    email_count = db.qry("select email from users where email = '{}'".format(value.strip()), fetch="rowcount")
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
        results = db.qry(query, arguments, fetch="one", commit=True)
        return results, 201


LOGIN_PARSER = reqparse.RequestParser(bundle_errors=True)
LOGIN_PARSER.add_argument('email', required=True)
LOGIN_PARSER.add_argument('password', required=True)


class LoginUser(Resource):
    def post(self):
        args = LOGIN_PARSER.parse_args()
        query = "select account_id, first_name, last_name, email, password_hash from users where  email = '{}';".format(
            args['email'])
        results = db.qry(query, fetch="one")
        if not results:
            return {"Error": "Email not registered"}, 404
        elif check_password_hash(results['password_hash'], args['password']):
            results.pop("password_hash")
            auth_token = auth.encode_auth_token(str(results["account_id"])).decode()
            results["auth_token"] = auth_token
            return results, 200
        else:
            return {"Error": "Wrong password"}, 400


api.add_resource(QuestionsApi, '/api/v1/questions/')
api.add_resource(QuestionGetUpdateDelete, '/api/v1/questions/<int:question_id>/')
api.add_resource(RegisterUser, '/api/v1/auth/signup/')
api.add_resource(LoginUser, '/api/v1/auth/login/')
api.add_resource(PostAnswer,'/api/v1/questions/<int:question_id>/answers/')
api.add_resource(UpdateAnswer, '/api/v1/questions/<int:question_id>/answers/<answer_id>/')
if __name__ == '__main__':
    app.run(debug=True)
