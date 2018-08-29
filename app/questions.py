from flask_restful import reqparse, Resource

from app.db import DatabaseConfig
from app.auth import Authentication

db = DatabaseConfig()
auth = Authentication()


def valid_question(value, name):
    value = value.strip()
    text_len = len(value)
    if 5 >= text_len <= 2000:
        raise ValueError(
            "The parameter '{}' must be between 5 and 2000 characters. Your value len is:{}".format(name, text_len))
    return value


QUESTION_PARSER = reqparse.RequestParser(bundle_errors=True)
QUESTION_PARSER.add_argument('question_subject', required=True, type=valid_question)
QUESTION_PARSER.add_argument('question_body', required=True, type=valid_question,
                             help="Question body is required")
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
        questions = db.qry("select  * from questions order by date_posted desc", fetch="all")
        for j in questions:
            j["date_posted"] = str(j["date_posted"])
        return questions, 200

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

        user_id = auth.jwt_required(args)
        try:
            user_id = int(user_id)
        except ValueError as e:
            return {"Error": "You have to be logged in"}, 403
        query = "INSERT into questions (question_subject, question_body, posted_by)" \
                " VALUES (%s, %s, %s)returning question_id, question_subject, " \
                "question_body, posted_by, date_posted"
        arguments = (
            args['question_subject'], args['question_body'], user_id)
        results = db.qry(query, arguments, fetch="one", commit=True)
        results["date_posted"] = str(results["date_posted"])
        return results, 201


def check_question_owner(question_id):
    query = "select users.account_id from questions inner join users on " \
            "(account_id=posted_by) where question_id = {}".format(question_id)
    question_result = db.qry(query, fetch="one")
    if question_result:
        return db.qry(query, fetch="one")["account_id"]


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

        question = db.qry("select  * from questions where question_id = "
                          "'{}'".format(question_id), fetch="one")
        if not question:
            return {"Error": "No question found"}, 404
        answers = db.qry("select  * from answers where question_id ="
                         " {}".format(question["question_id"]), fetch="all")
        for answer in answers:
            answer["answer_date"] = str(answer["answer_date"])
        question["date_posted"] = str(question["date_posted"])
        question["answers"] = answers
        return question, 200

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
        user_id = auth.jwt_required(args)
        try:
            user_id = int(user_id)
        except ValueError as e:
            return {"Error": user_id}, 400
        check_question = check_question_owner(question_id)
        if not check_question:
            return {"Error": "Question not found"}, 404
        if not user_id == check_question:
            return {"Error": "UnAuthorised"}, 401
        query = "DELETE FROM questions WHERE question_id = {};".format(question_id)
        question = db.qry(query, commit=True)
        return question, 204

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

        user_id = auth.jwt_required(args)
        try:
            user_id = int(user_id)
        except ValueError as e:
            return {"Error": "You have to be logged in"}
        if not user_id == check_question_owner(question_id):
            return {"Error": "UnAuthorised"}, 401
        params = args['question_subject'], args['question_body'], question_id
        query = "UPDATE questions SET question_subject = %s, " \
                "question_body = %s WHERE question_id = %s " \
                "RETURNING question_id, question_subject, " \
                "question_body, posted_by, date_posted;"
        question = db.qry(query, params, fetch="one")
        if not question:
            return {"Error": "No question found"}, 404
        question["date_posted"] = str(question["date_posted"])
        return question, 200
