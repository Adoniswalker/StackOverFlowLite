"""This module is used to test user"""
import json

from basement import TestStackBase


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

    def test_valid_logout(self):
        """ Test for logout before token expires """
        resp_register = self.client_app.post(
            '/api/v1/auth/signup/',
            data=json.dumps(dict(
                email='joetestmail@gmail.com',
                password='123456uij'
            )),
            content_type='application/json',
        )
        # import pdb; pdb.set_trace()
        data_register = json.loads(resp_register.data.decode())
        self.assertTrue(data_register['email'] == 'joetestmail@gmail.com')
        self.assertTrue(data_register['first_name'] is None)
        self.assertTrue(data_register['last_name'] is None)
        self.assertTrue(resp_register.content_type == 'application/json')
        self.assertEqual(resp_register.status_code, 201)
        # user login
        resp_login = self.client_app.post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                email='joetestmail@gmail.com',
                password='123456uij'
            )),
            content_type='application/json'
        )
        data_login = json.loads(resp_login.data.decode())
        self.assertTrue(data_login['email'] == 'joetestmail@gmail.com')
        self.assertTrue(data_login['auth_token'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, 200)
        # valid token logout
        response = self.client_app.post(
            '/api/v1/auth/logout/',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    resp_login.data.decode()
                )['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged out.')
        self.assertEqual(response.status_code, 200)

    def test_logout_blacksted_token(self):
        resp_register = self.client_app.post(
            '/api/v1/auth/signup/',
            data=json.dumps(dict(
                email='joetestmail@gmail.com',
                password='123456uij'
            )),
            content_type='application/json',
        )
        # import pdb; pdb.set_trace()
        data_register = json.loads(resp_register.data.decode())
        self.assertTrue(data_register['email'] == 'joetestmail@gmail.com')
        self.assertTrue(data_register['first_name'] is None)
        self.assertTrue(data_register['last_name'] is None)
        self.assertTrue(resp_register.content_type == 'application/json')
        self.assertEqual(resp_register.status_code, 201)
        # user login
        resp_login = self.client_app.post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                email='joetestmail@gmail.com',
                password='123456uij'
            )),
            content_type='application/json'
        )
        data_login = json.loads(resp_login.data.decode())
        self.assertTrue(data_login['email'] == 'joetestmail@gmail.com')
        self.assertTrue(data_login['auth_token'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, 200)
        # valid token logout
        response = self.client_app.post(
            '/api/v1/auth/logout/',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    resp_login.data.decode()
                )['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged out.')
        self.assertEqual(response.status_code, 200)
        response_out_again = self.client_app.post(
            '/api/v1/auth/logout/',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    resp_login.data.decode()
                )['auth_token']
            )
        )
        data_logout = json.loads(response_out_again.data.decode())
        assert data_logout["message"]["Authorization"] == "You are logged out, Kindly login again"
        assert response_out_again.status_code == 400
        assert resp_login.content_type == 'application/json'