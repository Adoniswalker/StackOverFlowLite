"""This file serves the endpoints"""
from flasgger import Swagger
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource, reqparse

from app import app
from app.db import DatabaseConfig
from app.answers import PostAnswer, UpdateAnswer
from app.models import Users
from app.questions import QuestionsApi, QuestionGetUpdateDelete

api = Api(app)
b_crypt = Bcrypt(app)
swagger = Swagger(app)
db_obj = DatabaseConfig()
user = Users()
app.config['SWAGGER'] = {
    'title': 'Stackoverflow-lite RESTful documentation',
    'uiversion': 2
}

REGISTER_PARSER = reqparse.RequestParser(bundle_errors=True)
REGISTER_PARSER.add_argument('first_name')
REGISTER_PARSER.add_argument('last_name')
REGISTER_PARSER.add_argument('email', required=True, type=user.email_address)
REGISTER_PARSER.add_argument('password', required=True, type=user.password_valid)


class RegisterUser(Resource):
    def post(self):
        """Endporint for user registration
        This is using docstrings for specifications.
        ---
        tags:
            - User
        consumes:
            - "application/json"
        produces:
            - "application/json"
        parameters:
            -   in: body
                name: body
                required: True
                description: User signup details
                schema:
                    id: UserSignUp
                    properties:
                        first_name:
                            required: False
                            description: The name of user
                            type: string
                            default: dennis

                        last_name:
                            required: False
                            description: The last name of user
                            type: string
                            default: jemo

                        email:
                            required: True
                            type: string
                            description: The email of user

                        password:
                            required: True
                            description: User provided answer
                            type: string
        responses:
            202:
                description: Successful registration
            400:
                description: Wrong details provided
        """
        args = REGISTER_PARSER.parse_args()
        return user.save(args), 201


LOGIN_PARSER = reqparse.RequestParser(bundle_errors=True)
LOGIN_PARSER.add_argument('email', required=True)
LOGIN_PARSER.add_argument('password', required=True)


class LoginUser(Resource):
    def post(self):
        """Endpoint for user login
        ---
        tags:
            -   User
        consumes:
            -   "application/json"
        produces:
            -   "application/json"
        parameters:
            -   in: body
                name: body
                required: True
                description: User login details
                schema:
                    id: UserLogin
                    properties:
                        email:
                            required: True
                            description: The email of user
                            type: string
                            default: dennisndsjfdj@ghdfj.djd

                        password:
                            required: True
                            description: User provided answer
                            type: string
                            default: dennsasdsis

        responses:
            200:
                description: User is succefully logged in
            400:
                description: When the user has not provide any details
                """

        args = LOGIN_PARSER.parse_args()
        return user.login(args)


api.add_resource(QuestionsApi, '/api/v1/questions/')
api.add_resource(QuestionGetUpdateDelete, '/api/v1/questions/<int:question_id>/')
api.add_resource(RegisterUser, '/api/v1/auth/signup/')
api.add_resource(LoginUser, '/api/v1/auth/login/')
api.add_resource(PostAnswer, '/api/v1/questions/<int:question_id>/answers/')
api.add_resource(UpdateAnswer, '/api/v1/questions/<int:question_id>/answers/<answer_id>/')
if __name__ == '__main__':
    app.run(debug=True)
