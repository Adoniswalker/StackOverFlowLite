import json
import unittest

from app import app, views
from app.db import DatabaseConfig

db = DatabaseConfig()


class TestStackBase(unittest.TestCase):
    """
    This class is used to test questions
    """


    def setUp(self):
        """
        Used in setting up before doing the testcases
        """
        with app.app_context():
            db.create_all()
        self.client_app = views.app.test_client()
        self.client_app.post(
            '/api/v1/auth/signup/',
            data=json.dumps(dict(
                last_name='james',
                email='joe4@gmail.com',
                password='123456sddfdf'
            )),
            content_type='application/json'
        )
        response = self.client_app.post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                email='joe4@gmail.com',
                password='123456sddfdf',
            )),
            content_type='application/json'
        )

        self.token = json.loads(response.data.decode())["auth_token"]
        question = {
            "question_subject": "What is computer programming?",
            "question_body": "It is important to note that jobs do not share storage, as each job runs in a "
                             "fresh VM or"}

        response = self.client_app.post("/api/v1/questions/",
                                       data=json.dumps(question),
                                       content_type="application/json", headers={'Authorization': self.token})
        self.question_id = json.loads(response.data.decode())["question_id"]

    def tearDown(self):
        """
        Used to reset or delete the database
        """
        with app.app_context():
            db.drop_all()
