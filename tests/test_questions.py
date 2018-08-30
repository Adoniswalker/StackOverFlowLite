"""This file is used for testcases"""
import json

from tests import TestStackBase


class TestQuestions(TestStackBase):

    def test_get_questions(self):
        """Start with a blank database."""
        response = self.client_app.get('/api/v1/questions/')
        assert response.is_json is True

    def test_post_question(self):
        """
        Tests a user can post a question.
        """
        question = {
            "question_subject": "Is this a new question subject?",
            "question_body": "It that jobs do not share storage, as each job runs in a "
                             "fresh VM or working on anything"}

        response = self.client_app.post("/api/v1/questions/",
                                        data=json.dumps(question),
                                        content_type="application/json", headers={'Authorization': self.token})
        data = json.loads(response.data.decode())
        self.assertTrue(data['question_subject'] == 'Is this a new question subject?')
        self.assertTrue(data[
                            'question_body'] == "It that jobs do not share storage, as each job runs in a "
                                                "fresh VM or working on anything")
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_post_question_without_token(self):
        """
        Tests a user can post a question.
        """
        question = {
            "question_subject": "Can i post a  question without a token?",
            "question_body": "It no you cant that jobs do not share storage, as each job runs in a "
                             "fresh VM or"}

        response = self.client_app.post("/api/v1/questions/",
                                        data=json.dumps(question),
                                        content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertTrue(data['message']['Authorization'] == 'Token is required. Please login')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_question_empty_body(self):
        """
        Tests user cannnot ask a question without body content
        """
        question = {
            "question_subject": "Can i post the subject only?",
        }

        response = self.client_app.post("/api/v1/questions/",
                                        data=json.dumps(question),
                                        content_type="application/json", headers={'Authorization': self.token})
        data = json.loads(response.data.decode())
        # import pdb;pdb.set_trace()
        self.assertTrue(data['message'][
                            'question_body'] == 'Missing required parameter in the JSON body or the post body or the query string')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_question_no_subject(self):
        """
        Check if question can be added without function
        """
        question = {
            "question_body": "It is important to note that jobs do not share storage, as each job runs in a "
                             "fresh VM or"}

        response = self.client_app.post("/api/v1/questions/",
                                        data=json.dumps(question),
                                        content_type="application/json", headers={'Authorization': self.token})
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'][
                            'question_subject'] == 'Missing required parameter in the JSON body or the post body or the query string')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_one_question_by_id(self):
        """
        Tests a user can get a question by id.
        """
        response = self.client_app.get("/api/v1/questions/{}/".format(self.question_id))
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertTrue(response.content_type == 'application/json')
        assert response_msg["question_subject"] == "What is computer programming?"
        assert response.status_code == 200

    def test_get_question_no_id(self):
        """Used to test what code is returned when getting question with no id"""
        response = self.client_app.get("/api/v1/questions/1000/")
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertTrue(response.content_type == 'application/json')
        assert response_msg["Error"] == "No question found"
        assert response.status_code == 404

    def test_delete_question_no_id(self):
        """
        Test to deleting non existing question
        """
        response = self.client_app.delete("/api/v1/questions/10000/", headers={'Authorization': self.token})
        assert response.status_code == 404

    def test_delete_question_no_token(self):
        """
        Test to deleting non existing question
        """
        response = self.client_app.delete("/api/v1/questions/1/")
        response_data = json.loads(response.data.decode("UTF-8"))
        assert response.content_type == 'application/json'

        assert response_data["message"]["Authorization"] == 'Token is required. Please login'
        assert response.status_code == 400

    def test_update_question(self):
        """
        This will test question update
        """
        response = self.client_app.put("/api/v1/questions/{}/".format(self.question_id),
                                       data=json.dumps(dict(question_subject="I prefer RAM",
                                                            question_body="This is question body")),
                                       content_type="application/json",
                                       headers={'Authorization': self.token})
        response_data = json.loads(response.data.decode("UTF-8"))
        assert response_data["question_subject"] == "I prefer RAM"
        assert response_data["question_body"] == "This is question body"
        assert response.status_code == 200

    def test_update_question_no_id(self):
        """
        This will test update of non existing question
        """
        response = self.client_app.put("/api/v1/questions/1000/",
                                       data=json.dumps(dict(question_subject="I prefer RAM",
                                                            question_body="This is question body")),
                                       content_type="application/json",
                                       headers={'Authorization': self.token})
        response_data = json.loads(response.data.decode("UTF-8"))
        assert response_data["Error"] == "UnAuthorised"
        assert response.status_code == 401
