"""This file is used to manipulate questions"""
from flask_restful import Resource, reqparse

from app import db
from app.auth import jwt_required

ANSWER_PARSER = reqparse.RequestParser(bundle_errors=True)
ANSWER_PARSER.add_argument('answer', required=True)
ANSWER_PARSER.add_argument('Authorization', location='headers',
                           required=True, help="You have to be looged in")

PUT_PARSER_ANSWER = reqparse.RequestParser(bundle_errors=True)
PUT_PARSER_ANSWER.add_argument('answer')
PUT_PARSER_ANSWER.add_argument('vote', type=int)
PUT_PARSER_ANSWER.add_argument('Authorization', location='headers',
                               required=True, help="You have to be logged in")


def is_question_owner(question_id, poster, vote, answer_id):
    """
    Used to check if user is owner of question and accept it
    :param question_id:
    :param poster:
    :param vote:
    :param answer_id:
    :return:
    """
    query = "select users.account_id from questions inner join users " \
            "on (questions.posted_by = users.account_id) where " \
            "questions.question_id={};".format(question_id)
    results = db.qry(query, fetch="one")
    if not poster == results["account_id"]:
        return {"Error": "Authorised user"}
    if not vote == 1:
        return {"Error": "Vote is required"}
    update_query = "update answers set answers.accepted = TRUE where answer_id = {}; " \
                   "answer_id, question_id, answeres_by, answer_date, answer," \
                   " accepted ".format(answer_id)
    return db.qry(update_query, commit=True, fetch="one")


def is_answer_owner(answer_id, poster, answer):
    """
    used to check if user is owner of answer and change the answer
    :param answer_id:
    :param poster:
    :param answer:
    :return:
    """
    query = "select users.account_id from answers inner join users " \
            "on (answers.answeres_by = users.account_id) where " \
            "answers.answer_id={};".format(answer_id)
    results = db.qry(query, fetch="one")
    if not poster == results["account_id"]:
        return {"Error": "Authorised user"}
    if not answer.strip():
        return {"Error": "Answer is required"}
    params = answer.strip(), answer_id
    update_query = "update answers set answer = %s where answer_id = %s returning " \
                   "answer_id, question_id, answeres_by, answer_date, answer," \
                   " accepted "
    return db.qry(update_query, params, commit=True, fetch="one")


class UpdateAnswer(Resource):
    def put(self, question_id, answer_id):
        """
        used to accept put request
        :param question_id:
        :param answer_id:
        :return:
        """
        args = PUT_PARSER_ANSWER.parse_args()
        user_id = jwt_required(args)
        try:
            user_id = int(user_id)
        except ValueError as e:
            return {"Error": user_id}
        # try:
        question_response = is_question_owner(question_id, user_id, args["vote"],
                                              answer_id)
        if question_response.get("answer_id"):
            question_response["answer_date"] = str(question_response["answer_date"])
            return question_response, 202
        answer_response = is_answer_owner(answer_id, user_id, args["answer"])
        if answer_response.get("answer_id"):
            answer_response["answer_date"] = str(answer_response["answer_date"])
            return answer_response, 201
        else:
            return question_response, 400


def is_question_exist(value):
    """
    used to check if question exist
    :param value:
    :return:
    """
    question_count = db.qry("select question_id from questions where "
                            "question_id = '{}'".format(value), fetch="rowcount")
    if question_count >= 1:
        return True


class PostAnswer(Resource):
    def post(self, question_id):
        """
        Used to add an answer
        :param question_id:
        :return:
        """
        if not is_question_exist(question_id):
            return {"Error": "No question found"}, 400
        args = ANSWER_PARSER.parse_args()

        user_id = jwt_required(args)
        try:
            user_id = int(user_id)
        except ValueError as e:
            return {"Error": user_id}
        query = "INSERT into answers (question_id, answeres_by, answer)" \
                " VALUES (%s, %s, %s) returning answer_id, question_id, " \
                "answeres_by, answer_date, answer, accepted "
        arguments = (question_id, user_id, args['answer'])
        results = db.qry(query, arguments, fetch="one", commit=True)
        results["answer_date"] = str(results["answer_date"])
        return results, 201
