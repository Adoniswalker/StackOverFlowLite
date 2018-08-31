import json
import unittest

from app import app, views
from app.db import DatabaseConfig

db = DatabaseConfig()


class TestStackBase(unittest.TestCase):
    """
    This class is used to test questions
    """

    @classmethod
    def setUpClass(cls):
        """
        Used in setting up before doing the testcases
        """
        with app.app_context():
            db.create_all()
        cls.client_app = views.app.test_client()
        with cls.client_app:
            cls.client_app.post(
                '/api/v1/auth/signup/',
                data=json.dumps(dict(
                    last_name='james',
                    email='joe4@gmail.com',
                    password='123456sddfdf'
                )),
                content_type='application/json'
            )
            response = cls.client_app.post(
                '/api/v1/auth/login/',
                data=json.dumps(dict(
                    email='joe4@gmail.com',
                    password='123456sddfdf',
                )),
                content_type='application/json'
            )

        cls.token = json.loads(response.data.decode())["auth_token"]
        question = {
            "question_subject": "What is computer programming?",
            "question_body": "It is important to note that jobs do not share storage, as each job runs in a "
                             "fresh VM or"}

        response = cls.client_app.post("/api/v1/questions/",
                                       data=json.dumps(question),
                                       content_type="application/json", headers={'Authorization': cls.token})
        cls.question_id = json.loads(response.data.decode())["question_id"]

    @classmethod
    def tearDownClass(cls):
        """
        Used to reset or delete the database
        """
        with app.app_context():
            db.drop_all()
