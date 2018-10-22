from flask import request

from app import app
from app.auth import Authentication
from app.db import DatabaseConfig
from flask_bcrypt import Bcrypt

from app.models import get_username

db = DatabaseConfig()
b_crypt = Bcrypt(app)
auth = Authentication()


class Question:
    """This class manipulates the question"""

    def get_all_questions(self):
        """
        Get all questions
        :return:
        """
        questions = db.qry("select answer_obj.*, u.first_name, u.last_name, u.email, "
                           "(select count(a.question_id) from answers a "
                           "where answer_obj.question_id= a.question_id) as answers"
                           " from questions answer_obj inner join users u on(answer_obj.posted_by ="
                           " u.account_id) order by answer_obj.date_posted asc",
                           fetch="all")
        if not questions:
            return questions, 404
        for question in questions:
            question["date_posted"] = str(question["date_posted"])
            question["url"] = request.host_url + "api/v1/questions/" + str(question["question_id"]) + "/"
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
                          "on(al.posted_by = u.account_id);", (question_id,), fetch="one")

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
            answer["url"] = f"{request.url_root}api/v1/questions/{str(answer['question_id'])}" \
                            f"/answers/{str(answer['answer_id'])}/"
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