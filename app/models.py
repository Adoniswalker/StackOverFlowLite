"""This module manipulates the different models"""
import psycopg2
import re

from app import app
from app.auth import Authentication
from app.db import DatabaseConfig
from flask_bcrypt import Bcrypt, check_password_hash

db = DatabaseConfig()
b_crypt = Bcrypt(app)
auth = Authentication()


class Users:
    def __init__(self):
        pass

    def save(self, args):
        """
        Will add new user to database
        :param args:
        :return:
        """
        query = "insert into users (first_name, last_name, email, password_hash)" \
                " values (%s,%s,%s, %s) returning account_id, first_name, last_name,  email"
        arguments = (
            args['first_name'], args['last_name'], args['email'],
            b_crypt.generate_password_hash(args['password']).decode('utf-8'))
        user = db.qry(query, arguments, fetch="one", commit=True)
        user["message"] = "You have succefully signed up"
        return user

    def email_address(self, value, name):
        """
        Will validate an email
        :param value:
        :param name:
        :return:
        """
        is_mail = self.is_email_valid(value, name)
        if not is_mail == value:
            return is_mail
        email_count = db.qry("select email from users where email ="
                             " '{}'".format(value.strip()), fetch="rowcount")
        if email_count >= 1:
            raise ValueError("'{}' has already been registered".format(value.strip()))
        return value

    def is_email_valid(self, email, name):
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email.strip()):
            raise ValueError("The parameter '{}' is not a valid email."
                             " You gave us the value:{}".format(name, email))
        return email

    def logout(self, token):
        query = "insert into blacklisttoken (token)values (%s)"
        # import pdb; pdb.set_trace()
        token = token.split(' ')[-1].strip()
        arguments = (token,)
        try:
            db.qry(query, arguments, commit=True)
        except psycopg2.IntegrityError as e:
            pass
        return {
                   'status': 'success',
                   'message': 'Successfully logged out.'
               }, 200

    def password_valid(self, value, name):
        """
        Validate a password provided
        :param value:
        :param name:
        :return:
        """
        password_regex = r"(?=.{8,})"
        if not re.match(password_regex, value.strip()):
            raise ValueError(
                "The parameter '{}' must be 8 characters or more. "
                "Your password length is:{}".format(name, len(value)))
        return value

    def login(self, args):
        """
        Processs the user login
        :param args:
        :return:
        """
        query = "select account_id, first_name, last_name, email, " \
                "password_hash from users where  email = '{}';".format(args['email'])
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


class Question:
    """This class manipulates the question"""

    def __init__(self):
        pass

    def get_all_questions(self):
        """
        Get all questions
        :return:
        """
        questions = db.qry("select  * from questions order by date_posted desc", fetch="all")
        if not questions:
            return questions, 404
        for j in questions:
            j["date_posted"] = str(j["date_posted"])
        return questions

    def save(self, args):
        """
        Add new question to database
        :param args:
        :return:
        """
        user_id = auth.jwt_required(args)
        try:
            user_id = int(user_id)
        except ValueError as e:
            return {"Error": user_id}, 403
        query = "INSERT into questions (question_subject, question_body, posted_by)" \
                " VALUES (%s, %s, %s)returning question_id, question_subject, " \
                "question_body, posted_by, date_posted"
        arguments = (
            args['question_subject'], args['question_body'], user_id)
        # import pdb; pdb.set_trace()
        results = db.qry(query, arguments, fetch="one", commit=True)
        results["date_posted"] = str(results["date_posted"])
        return results, 201

    def get_one(self, question_id):
        """
        Get one question with details
        :param question_id:
        :return:
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

    def delete(self, question_id, args):
        """
        Delete a question
        :param question_id:
        :param args:
        :return:
        """
        user_id = auth.jwt_required(args)
        try:
            user_id = int(user_id)
        except ValueError as e:
            return {"Error": user_id}, 400
        check_question = self.check_question_owner(question_id)
        if not check_question:
            return {"Error": "Question not found"}, 404
        if not user_id == check_question:
            return {"Error": "UnAuthorised"}, 401
        query = "DELETE FROM questions WHERE question_id = {};".format(question_id)
        db.qry(query, commit=True)
        return {"message": "Succefully deleted the question"}, 200

    def check_question_owner(self, question_id):
        """
        Return the owner of the question
        :param question_id:
        :return:
        """
        query = "select users.account_id from questions inner join users on " \
                "(account_id=posted_by) where question_id = {}".format(question_id)
        question_result = db.qry(query, fetch="one")
        if question_result:
            return db.qry(query, fetch="one")["account_id"]

    # def check_valid_paragraph(self, text):
    #     # regex = '^(?!.*([A-Za-z0-9@])\1{2})(?=.*[a-zA-Z])(?=.*\d)[A-Za-z0-9\s@.]+$'
    #     if not re.match("^[a-zA-Z0-9/.\s?_"']{5,2000}$") , text):
    #         raise ValueError(
    #             "Question must contain aleast one alphabet, not more that "
    #             "two characters in a row, and only @. ")
    #     return text

    def check_question_posted(self, value):
        """
        Check if the qwuestion has been asked before
        :param value:
        :return:
        """
        query = "select question_id from questions where question_subject ='{0}' " \
                "or question_body='{0}';".format(value)
        return db.qry(query, fetch="all")

    def update(self, question_id, args):
        """
        Update the questions
        :param question_id:
        :param args:
        :return:
        """
        user_id = auth.jwt_required(args)
        try:
            user_id = int(user_id)
        except ValueError as e:
            return {"Error": user_id}
        if not user_id == self.check_question_owner(question_id):
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

    def valid_question(self, value, name):
        """
        Validate the question
        :param value:
        :param name:
        :return:
        """
        value = value.strip()
        text_len = len(value)
        if 5 > text_len < 2000:
            raise ValueError(
                "The parameter '{}' must be between 5 and 2000 characters. "
                "and contain only alphabets, numeric, /, .,?,_ "
                "Your value len is:{}".format(name, text_len))
        asked = self.check_question_posted(value)
        if asked:
            raise ValueError("'{}' has already been asked here {}".format(value, asked))
        return value

    def get_user_question(self, user_id):
        """
                Get one question with details
                :param question_id:
                :return:
                """
        questions = db.qry("select  * from questions where posted_by = "
                           "'{}' order by date_posted desc".format(user_id), fetch="all")
        for question in questions:
            question["date_posted"] = str(question["date_posted"])
        return questions


class Answer:
    """This class manipulates the answer"""

    def __init__(self):
        pass

    def save(self, question_id, args):
        """
        Save a new answer
        :param question_id:
        :param args:
        :return:
        """
        if not self.is_question_exist(question_id):
            return {"Error": "No question found"}, 400
        user_id = auth.jwt_required(args)
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

    def update(self, question_id, answer_id, args):
        """
        Update an answer
        :param question_id:
        :param answer_id:
        :param args:
        :return:
        """
        user_id = auth.jwt_required(args)
        try:
            user_id = int(user_id)
        except ValueError as e:
            return {"Error": user_id}
        question_response = self.is_question_owner(question_id, user_id, args["vote"],
                                                   answer_id)
        if question_response[0] is None:
            return {"Error": "Answer not found"}, 404
        if question_response[0].get("answer_id"):
            question_response[0]["answer_date"] = str(question_response[0]["answer_date"])
            return question_response
        answer_response = self.is_answer_owner(answer_id, user_id, args["answer"])
        if answer_response[0].get("answer_id"):
            answer_response[0]["answer_date"] = str(answer_response[0]["answer_date"])
            return answer_response
        else:
            return question_response

    def is_question_exist(self, value):
        """
        used to check if question exist
        :param value:
        :return:
        """
        question_count = db.qry("select question_id from questions where "
                                "question_id = '{}'".format(value), fetch="rowcount")
        if question_count >= 1:
            return True

    def is_question_owner(self, question_id, poster, vote, answer_id):
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
        if not results:
            return {"Error": "Question not found"}, 404
        if not poster == results["account_id"]:
            return {"Error": "UnAuthorised user"}, 401
        if not vote == 1:
            return {"Error": "Vote is required"}, 400
        params = (answer_id,)
        update_query = "update answers set accepted = TRUE where answer_id = %s returning " \
                       "answer_id, question_id, answeres_by, answer_date, answer," \
                       " accepted "
        return db.qry(update_query, params, commit=True, fetch="one"), 200

    def is_answer_owner(self, answer_id, poster, answer):
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
        if not results:
            return {"Error": "Answer not found"}, 404
        if not poster == results["account_id"]:
            return {"Error": "UnAuthorised user"}, 401

        if not answer:
            return {"Error": "Answer is required"}, 400
        params = answer.strip(), answer_id
        update_query = "update answers set answer = %s where answer_id = %s returning " \
                       "answer_id, question_id, answeres_by, answer_date, answer," \
                       " accepted "
        return db.qry(update_query, params, commit=True, fetch="one"), 200
