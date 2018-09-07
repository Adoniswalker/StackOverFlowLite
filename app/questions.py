from flask_restful import reqparse, Resource

from app.db import DatabaseConfig
from app.auth import Authentication
from app.models import Question

db = DatabaseConfig()
auth = Authentication()

quest = Question()

QUESTION_PARSER = reqparse.RequestParser(bundle_errors=True)
QUESTION_PARSER.add_argument('question_subject', required=True, type=quest.valid_question)
QUESTION_PARSER.add_argument('question_body', required=True, type=quest.valid_question)
QUESTION_PARSER.add_argument('Authorization', location='headers', required=True,
                             help="Token is required. Please login")

TOKEN_PARSER = reqparse.RequestParser(bundle_errors=True)
TOKEN_PARSER.add_argument('Authorization', location='headers',
                          required=True, help="Token is required. Please login")


class QuestionsApi(Resource):
    def get(self):
        """
        This endponint will get all the questions
        :return:
        This endpoint will fetch one question
        :rtype: jsonify
        This one will get a single question when id is provided
        ---
        tags:
            - Question
        responses:
            200:
                description: The details for a question
            """
        return quest.get_all_questions()

    def post(self):
        """
        This method will post a new answer
        ---
        tags:
            - Question
        consumes:
            - "application/json"
        produces:
            - "application/json"
        parameters:
            -   in: header
                name: Authorization
                type: string
                required: true

            -   in: body
                name: body
                required: True
                description: The question subject and title
                schema:
                    id: QuestionPut
                    properties:
                        question_subject:
                            type: string
                            required: True
                            description: What is the question about

                        question_body:
                            type: string
                            required: True
                            description: The whole question

        responses:
            200:
                description: Question was succefully posted
            400:
               description: Missing details for question

        :return:
        """
        args = QUESTION_PARSER.parse_args()
        return quest.save(args)


class QuestionGetUpdateDelete(Resource):
    def get(self, question_id):
        """
        This endpoint will fetch one question
        :rtype: jsonify
        This one will get a single question when id is provided
        ---
        tags:
            - Question Detail
        parameters:
            -   in: path
                name: question_id
                required: true
                description: The ID of the question, try 42!
                type: string
        responses:
            200:
                description: The details fo a question
                schema:
                    id: Question
                    properties:
                        posted_by:
                            type: int
                            description: The user who posted the question
                        date_posted:
                            type: string
                        question_subject:
                            type: string
                        question_id:
                            type: int
                            description: The question unique id
                        question_body:
                            type: string
                            description: Content of question
            """

        return quest.get_one(question_id)

    def delete(self, question_id):
        """
            This function will delete a question
            :param question_id:
            :return:
        ---
        tags:
         -  Question Detail

        produces:
          - "application/json"
        parameters:
            -   name: question_id
                in: path
                description: Id of question to be deleted
                required: true
                type: "integer"
                format: "int64"
            -   in: header
                name: Authorization
                type: string
                required: true
        responses:
            204:
                description: Question deleted successfull
            400:
                description: "Invalid ID supplied"
            404:
                description: "Question not found"
            """
        args = TOKEN_PARSER.parse_args()
        return quest.delete(question_id, args)

    def put(self, question_id):
        """
            This endpont will update subject and body when called
            :param question_id:
            :return:

        ---
        tags:
            - Question Detail
        consumes:
            - "application/json"
        produces:
            - "application/json"
        parameters:

            -   in: path
                name: question_id
                required: True
                description: The question id

            -   in: header
                name: Authorization
                type: string
                required: true

            -   in: body
                name: body
                required: True
                description: The question subject and title
                schema:
                    id: QuestionPut
                    properties:
                        question_subject:
                            type: str
                            required: True
                        question_body:
                            type: str
                            required: True

        responses:
            200:
               description: Question updated successful
            400:
               description: Missikng parameters in the questions
            """
        args = QUESTION_PARSER.parse_args()
        return quest.update(question_id, args)


class UserQuestions(Resource):
    def get(self):
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
        args = TOKEN_PARSER.parse_args()
        user_id = auth.jwt_required(args)
        try:
            user_id = int(user_id)
        except ValueError as e:
            return {"message": {"Authorization": user_id}}, 403
        return quest.get_user_question(user_id), 200

