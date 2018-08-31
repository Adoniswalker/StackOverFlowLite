"""This module is used to test user"""
import json

from tests import TestStackBase


class TestUser(TestStackBase):
    """
    This class is used to test questionsome
    """

    def test_registration(self):
        """ Test for user registration """
        response = self.client_app.post(
            '/api/v1/auth/signup/',
            data=json.dumps(dict(
                last_name='james',
                email='newjoe@gmail.com',
                password='123456sddfdf'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['email'] == 'newjoe@gmail.com')
        self.assertTrue(data['first_name'] is None)
        self.assertTrue(data['last_name'] == 'james')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        """
        This method will test user login
        """
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
        self.assertTrue(data['email'] == 'joe@gmail.com')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        response = self.client_app.post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                email='jodfghe@gmail.com',
                password='123456'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['Error'] == 'Email not registered')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 404)
