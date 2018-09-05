import unittest

from app.auth import Authentication

auth = Authentication()


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.valid_token = auth.encode_auth_token(5).decode()
        self.invalid_token = "sadfghjgfdksjadfg"

    def test_encode_token(self):
        print(auth.encode_auth_token('7').decode())
        assert isinstance(auth.encode_auth_token('7').decode(), str )

    def test_decode_auth(self):
        assert auth.decode_auth_token(self.valid_token) == 5