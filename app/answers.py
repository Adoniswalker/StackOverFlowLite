"""This file is used to manipulate questions"""
from flask_restful import Resource, reqparse

from app.db import DatabaseConfig
from app.auth import Authentication
from app.models import Answer

answer = Answer()
auth = Authentication()
db = DatabaseConfig()

ANSWER_PARSER = reqparse.RequestParser(bundle_errors=True)
ANSWER_PARSER.add_argument('answer', required=True, type=answer.valid_answer)
ANSWER_PARSER.add_argument('Authorization', location='headers',
                           required=True, help="You have to be looged in")

PUT_PARSER_ANSWER = reqparse.RequestParser(bundle_errors=True)
PUT_PARSER_ANSWER.add_argument('answer')
PUT_PARSER_ANSWER.add_argument('vote', type=int)
PUT_PARSER_ANSWER.add_argument('Authorization', location='headers',
                               required=True, help="You have to be logged in")


class UpdateAnswer(Resource):
    def put(self, question_id, answer_id):
        """
        used to accept put request
        :param question_id:
        :param answer_id:
        :return:
        ---
        tags:
            - Answer
        consumes:
            - "application/json"
        produces:
            - "application/json"
        parameters:

            -   in: path
                name: question_id
                required: True
                description: The question id

            -   in: path
                name: answer_id
                required: True
                description: The answer id

            -   in: header
                name: Authorization
                type: string
                required: true

            -   in: body
                name: body
                required: True
                description: The question subject and title
                schema:
                    id: Answer
                    properties:
                        question_subject:
                            type: str
                            required: False

                        question_body:
                            type: str
                            required: False

        responses:
            200:
                description: Update was succeful
        """
        args = PUT_PARSER_ANSWER.parse_args()
        return answer.update(question_id, answer_id, args)


class PostAnswer(Resource):
    def post(self, question_id):
        """
        Used to add an answer
        :param question_id:
        :return:
        ---
        tags:
            - Answer
        consumes:
            - "application/json"
        produces:
            - "application/json"
        parameters:

            -   in: path
                name: question_id
                required: True
                description: The id of question to be answered

            -   in: header
                name: Authorization
                type: string
                required: true

            -   in: body
                name: body
                required: True
                description: The question subject and title
                schema:
                    id: Answer
                    properties:
                        answer:
                            type: str
                            required: True

        responses:
            200:
                description: Answer successful
        """

        args = ANSWER_PARSER.parse_args()
        return answer.save(question_id, args)
