"""This file is used for testcases"""
import json
import unittest

from app import views, app, db


# @pytest.fixture
# def client():
#     """This function is using for setting up test environment
#     :rtype: object
#     """
#     views.app.config['TESTING'] = True
#     client = views.app.test_client()
#     with views.app.app_context():
#         yield client
from app.ddl import ddl


class TestQuestions(unittest.TestCase):
    """
    This class is used to test questions
    """

    def setUp(self):
        """
        Used in setting up before doing the testcases
        """
        with app.app_context():
            # db.qry("drop TABLE answers; drop TABLE questions; drop TABLE users; ", commit=True);
            set_up = db.qry(ddl, commit=True)
        self.client_app = views.app.test_client()


    def get_token(self):
        with self.client_app:
            self.client_app.post(
                '/api/v1/auth/signup/',
                data=json.dumps(dict(
                    last_name='james',
                    email='joe@gmail.com',
                    password='123456sddfdf'
                )),
                content_type='application/json'
            )
            response = self.client_app.post(
                '/api/v1/auth/login/',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456sddfdf',
                )),
                content_type='application/json'
            )
        return json.loads(response.data.decode())["token"]

    def test_get_questions(self):
        """Start with a blank database."""
        response = self.client_app.get('/api/v1/questions/')
        assert response.is_json is True

    # def test_post_question(self):
    #     """
    #     Tests a user can post a question.
    #     """
    #     question = {
    #         "subject": "What is computer programming?",
    #         "body": "It is important to note that jobs do not share storage, as each job runs in a "
    #                 "fresh VM or"}
    #
    #     response = self.client_app.post("/api/v1/questions/",
    #                                     data=json.dumps(question),
    #                                     content_type="application/json")
    #     assert response.status_code == 201
    #
    # def test_post_question_empty_body(self):
    #     """
    #     Tests user cannnot ask a question without body content
    #     """
    #     response = self.client_app.post("/api/v1/questions/",
    #                                     data=json.dumps(dict(subject="how to delete git branch",
    #                                                          body="")),
    #                                     content_type="application/json")
    #     assert response.status_code == 400
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     assert response_msg["Error"] == "Please provide all fields with keys 'subject' and 'body'"
    #
    # def test_post_question_no_subject(self):
    #     """
    #     Check if question can be added without function
    #     """
    #     response = self.client_app.post("/api/v1/questions/",
    #                                     data=json.dumps(dict(subject="",
    #                                                          body="I want to delete"
    #                                                               " a branch both locally..")),
    #                                     content_type="application/json")
    #     assert response.status_code == 400
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     assert response_msg["Error"] == "Please provide all fields with keys 'subject' and 'body'"
    #
    # def test_get_one_question_by_id(self):
    #     """
    #     Tests a user can get a question by id.
    #     """
    #     response = self.client_app.get("/api/v1/questions/2/")
    #     assert response.status_code == 200
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     assert response_msg["subject"] == "Is using APIs good?"
    #
    # def test_get_question_no_id(self):
    #     """Used to test what code is returned when getting question with no id"""
    #     response = self.client_app.get("/api/v1/questions/1000/")
    #     assert response.status_code == 404
    #
    # def test_post_answer(self):
    #     """
    #     Test when posting an answer
    #     """
    #     response = self.client_app.post("/api/v1/questions/3/answers/",
    #                                     data=json.dumps(dict(answer="I prefer with ram")),
    #                                     content_type="application/json")
    #     assert response.status_code == 201
    #
    # def test_post_no_answer(self):
    #     """
    #     Testing a question without an answer
    #     """
    #     response = self.client_app.post("/api/v1/questions/1/answers/",
    #                                     data=json.dumps(dict(answer="")),
    #                                     content_type="application/json")
    #     assert response.status_code == 400
    #
    # def test_delete_question_no_id(self):
    #     """
    #     Test to deleting non existing question
    #     """
    #     response = self.client_app.delete("/api/v1/questions/10000/")
    #     assert response.status_code == 404
    #
    # def test_update_question(self):
    #     """
    #     This will test question update
    #     """
    #     response = self.client_app.put("/api/v1/questions/2/",
    #                                    data=json.dumps(dict(subject="I prefer RAM",
    #                                                         body="This is question body")),
    #                                    content_type="application/json")
    #     assert response.status_code == 200
    #
    # def test_update_question_no_id(self):
    #     """
    #     This will test update of non existing question
    #     """
    #     response = self.client_app.put("/api/v1/questions/10000/",
    #                                    data=json.dumps(dict(subject="I prefer RAM",
    #                                                         body="This is body")),
    #                                    content_type="application/json")
    #     assert response.status_code == 404
    #
    # def test_post_answer_with_no_id(self):
    #     """
    #     Test a question with non existing id
    #     """
    #     response = self.client_app.post("/api/v1/questions/10000/answers/",
    #                                     data=json.dumps(dict(answer="I prefer RAM")),
    #                                     content_type="application/json")
    #     assert response.status_code == 404
    #
    # def test_delete_question(self):
    #     """
    #     Test deleting an answer
    #     """
    #     response = self.client_app.delete("/api/v1/questions/1/")
    #     assert response.status_code == 204

    def tearDown(self):
        with app.app_context():
            db.qry("drop TABLE answers; drop TABLE questions; drop TABLE users; ", commit=True);


if __name__ == "__main__":
    unittest.main()
