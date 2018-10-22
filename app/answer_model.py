
from app import app
from app.auth import Authentication
from app.db import DatabaseConfig
from flask_bcrypt import Bcrypt

db = DatabaseConfig()
b_crypt = Bcrypt(app)
auth = Authentication()


class Answer:
    """This class manipulates the answer"""

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

    def delete(self, question_id, answer_id, params):
        user_id = auth.jwt_required(params)
        try:
            user_id = int(user_id)
        except ValueError as e:
            return {"message": {"Authorization": user_id}}, 403
        query = "select * from answers a where a.answer_id = %s"
        results = db.qry(query, (answer_id,), fetch="one")
        if not results:
            return {"message": {"answer": "Answer not found"}}, 404
        if not results["answeres_by"] == user_id:
            return {"message": {"answer": "You dont have permission to delete this answer"}}, 401
        delete_query = "delete from answers a where a.answer_id = %s and a.question_id = %s returning true"
        if db.qry(delete_query, (answer_id, question_id,), commit=True, fetch="one"):
            return {"message": {"answer": "Successfully deleted the answer"}}, 200
