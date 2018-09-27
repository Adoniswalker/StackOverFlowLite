"""This module manipulates the different models"""
import psycopg2
import re

from flask import request

from app import app
from app.auth import Authentication
from app.db import DatabaseConfig
from flask_bcrypt import Bcrypt, check_password_hash

db = DatabaseConfig()
b_crypt = Bcrypt(app)
auth = Authentication()


def get_username(first_name, last_name, email):
    if last_name or first_name:
        return first_name + " " + last_name
    else:
        return email.split("@")[0]


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
        email_count = db.qry("select email from users where email =%s",
                             (value.strip(),), fetch="rowcount")
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
                "password_hash from users where  email = %s;"
        results = db.qry(query, (args['email'],), fetch="one")
        if not results:
            return {"Error": "Email not registered"}, 404
        elif check_password_hash(results['password_hash'], args['password']):
            results.pop("password_hash")
            auth_token = auth.encode_auth_token(str(results["account_id"])).decode()
            results["auth_token"] = auth_token
            return results, 200
        else:
            return {"Error": "Wrong password"}, 400

    def get_user(self, user_id):
        question = db.qry("select u.account_id, u.first_name, u.last_name,u.email, "
                          "(select count(q.posted_by) from questions q where"
                          " q.posted_by = %s) as questions_counts,"
                          "(select count(a.answeres_by) from answers a where "
                          "a.answeres_by = %s) as answers_counts"
                          " from users u where u.account_id = %s;",
                          (user_id, user_id, user_id,), fetch="one")
        return question, 200


class Question:
    """This class manipulates the question"""

    def get_all_questions(self):
        """
        Get all questions
        :return:
        """
        questions = db.qry("select q.*, u.first_name, u.last_name, u.email, "
                           "(select count(a.question_id) from answers a "
                           "where q.question_id= a.question_id) as answers"
                           " from questions q inner join users u on(q.posted_by ="
                           " u.account_id) order by q.date_posted asc",
                           fetch="all")
        if not questions:
            return questions, 404
        for question in questions:
            question["date_posted"] = str(question["date_posted"])
            question["url"] = request.host_url+"api/v1/questions/"+str(question["question_id"])+"/"
            question["username"] = get_username(question["first_name"], question["last_name"], question["email"])
            del question["email"]
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
            return {"message": {"Authorization": user_id}}, 403
        query = "INSERT into questions (question_subject, question_body, posted_by)" \
                " VALUES (%s, %s, %s)returning question_id, question_subject, " \
                "question_body, posted_by, date_posted"
        arguments = (
            args['question_subject'], args['question_body'], user_id)
        results = db.qry(query, arguments, fetch="one", commit=True)
        results["date_posted"] = str(results["date_posted"])
        results["answers"] = 0
        return results, 201

    def get_one(self, question_id):
        """
        Get one question with details
        :param question_id:
        :return:
        """
        question = db.qry("select al.*, u.first_name, u.last_name, u.email from "
                          "(select qs.*, count(ars.question_id) as answers_no "
                          "from questions qs left join answers ars using "
                          "(question_id) where qs.question_id = %s group by qs.question_id order by "
                          "date_posted desc) al inner join users u "
                          "on(al.posted_by = u.account_id);", (question_id,),  fetch="one")
        
        if not question:
            return {"Error": "No question found"}, 404
        question["username"] = get_username(question["first_name"], question["last_name"], question["email"])
        del question["email"]
        answers = db.qry("select  ars.*, u.first_name, u.last_name, u.email"
                         " from answers ars inner join users u "
                         "on(ars.answeres_by=u.account_id) where ars.question_id =%s",
                         (question["question_id"],), fetch="all")
        for answer in answers:
            answer["answer_date"] = str(answer["answer_date"])
            answer["username"] = get_username(answer["first_name"], answer["last_name"], answer["email"])
            del answer["email"]
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
            return {"message": {"Authorization": user_id}}, 403
        check_question = self.check_question_owner(question_id)
        if not check_question:
            return {"message": {"question": "Question not found"}}, 404
        if not user_id == check_question:
            return {"message": {"Authorization": "You are not allowed to delete"}}, 401
        query = "DELETE FROM questions WHERE question_id = %s;"
        db.qry(query, (question_id,), commit=True)
        return {"message": {"question": "Successfully deleted the question"}}, 200

    def check_question_owner(self, question_id):
        """
        Return the owner of the question
        :param question_id:
        :return:
        """
        query = "select users.account_id from questions inner join users on " \
                "(account_id=posted_by) where question_id = %s"
        question_result = db.qry(query, (question_id,), fetch="one")
        if question_result:
            return question_result["account_id"]

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
        query = "select question_id from questions where question_subject =%s " \
                "or question_body=%s;"
        return db.qry(query, (value, value), fetch="all")

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
            return {"message": {"Authorization": user_id}}, 403
        if not user_id == self.check_question_owner(question_id):
            return {"message": {"Authorization": "You are not allowed to edit this question"}}, 401
        params = args['question_subject'], args['question_body'], question_id
        query = "UPDATE questions SET question_subject = %s, " \
                "question_body = %s WHERE question_id = %s " \
                "RETURNING question_id, question_subject, " \
                "question_body, posted_by, date_posted;"
        question = db.qry(query, params, fetch="one", commit=True)
        if not question:
            return {"message": {"question": "No question found"}}, 404
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
        questions = db.qry("select al.*, u.first_name, u.last_name, u.email "
                           "from (select qs.*, count(ars.question_id) as answers "
                           "from questions qs left join answers ars using "
                           "(question_id) group by qs.question_id order by "
                           "date_posted desc) al inner join users u on(al.posted_by = u.account_id) "
                           "where u.account_id = %s;", (user_id,), fetch="all")
        if not questions:
            return {"message": {"questions": "You don't have any questions"}}, 404
        for question in questions:
            question["date_posted"] = str(question["date_posted"])
            question["username"] = get_username(question["first_name"], question["last_name"], question["email"])
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
            return {"message": {"question": "No question found"}}, 404
        user_id = auth.jwt_required(args)
        try:
            user_id = int(user_id)
        except ValueError as e:
            return {"message": {"Authorization": user_id}}, 403
        query = "INSERT into answers (question_id, answeres_by, answer)" \
                " VALUES (%s, %s, %s) returning answer_id, question_id, " \
                "answeres_by, answer_date, answer, accepted "
        arguments = (question_id, user_id, args['answer'])
        results = db.qry(query, arguments, fetch="one", commit=True)
        results["answer_date"] = str(results["answer_date"])
        return results, 201

    def update(self, question_id, answer_id, answer_args):
        """
        Update an answer
        :param question_id:
        :param answer_id:
        :param answer_args:
        :return:
        """
        user_id = auth.jwt_required(answer_args)
        try:
            user_id = int(user_id)
        except ValueError as e:
            return {"message": {"Authorization": user_id}}, 403
        answer = answer_args["answer"]
        if answer_args["vote"] and answer:
            return {"message": {"vote": "Kindly provide one parameter to be filled"}}, 400
        if answer_args["vote"] is not None:
            return self.is_question_owner(question_id, user_id, answer_args["vote"], answer_id)
        if answer:
            return self.is_answer_owner(answer_id, user_id, answer_args["answer"])
        else:
            return {"message": {"vote": "Provide atleast one of this parameters 'vote' or 'answer' "}}, 400

    def is_question_exist(self, value):
        """
        used to check if question exist
        :param value:
        :return:
        """
        question_count = db.qry("select question_id from questions where "
                                "question_id = %s", (value,), fetch="rowcount")
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
                "questions.question_id=%s;"
        results = db.qry(query, (question_id,), fetch="one")
        if not results:
            return {"Error": "Question not found"}, 404
        if not poster == results["account_id"]:
            return {"Error": "UnAuthorised user"}, 401
        if vote:
            vote = True
        else:
            vote = False
        params = (vote, answer_id,)
        update_query = "update answers set accepted = %s where answer_id = %s returning " \
                       "answer_id, question_id, answeres_by, answer_date, answer," \
                       " accepted "
        question_response = db.qry(update_query, params, commit=True, fetch="one")
        question_response["answer_date"] = str(question_response["answer_date"])
        return question_response

    def valid_answer(self, value, name):
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
        asked = self.check_answer_posted(value)
        if asked:
            raise ValueError("'{}' has already been asked here {}".format(value, asked))
        return value

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
                "answers.answer_id=%s;"
        results = db.qry(query, (answer_id,), fetch="one")
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
        answer_response = db.qry(update_query, params, commit=True, fetch="one")
        answer_response["answer_date"] = str(answer_response["answer_date"])
        return answer_response

    def check_answer_posted(self, value):
        """
                Check if the answer has been provided before
                :param value:
                :return:
                """
        query = "select answer_id from answers where answer =%s"
        return db.qry(query, (value,), fetch="all")
