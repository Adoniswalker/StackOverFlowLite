"""This module is used to test user"""
import json
import unittest

from app import views, db, app


class TestQuestions(unittest.TestCase):
    """
    This class is used to test questionsome
    """

    def setUp(self):
        """
        Used in setting up before doing the testcases
        """
        with app.app_context():
            db.create_all()
        self.client_app = views.app.test_client()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_registration(self):
        """ Test for user registration """
        with self.client_app:
            response = self.client_app.post(
                '/api/v1/auth/signup/',
                data=json.dumps(dict(
                    last_name='james',
                    email='joe@gmail.com',
                    password='123456sddfdf'
                )),
                content_type='application/json'
            )
            # import pdb; pdb.set_trace()
            data = json.loads(response.data.decode())
            self.assertTrue(data['email'] == 'joe@gmail.com')
            self.assertTrue(data['first_name'] is None)
            self.assertTrue(data['last_name'] == 'james')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_login(self):
        """
        This method will test user login
        """
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
        data = json.loads(response.data.decode())
        # import pdb; pdb.set_trace()
        self.assertTrue(data['email'] == 'joe@gmail.com')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client_app:
            response = self.client_app.post(
                '/api/v1/auth/login/',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['Error'] == 'Email not registered')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
