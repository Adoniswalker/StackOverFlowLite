import datetime
import jwt

from app import app
from app.db import DatabaseConfig

db = DatabaseConfig()


class Authentication:
    def check_user_in_db(self, account_id):
        try:
            account_id = int(account_id)
            user_query = "select account_id from users where account_id = %s"
            if db.qry(user_query, (account_id,), fetch="one"):
                return True
        except ValueError:
            return account_id

    def jwt_required(self, f):
        """ Ensure jwt token is provided and valid
            :param f: function to decorated
            :return: decorated function
        """
        try:
            auth_header = f['Authorization'].split(' ')[-1]
        except Exception as e:
            print(e)
            return "Unauthorized. Please login {}".format(e)
        decode_result = self.decode_auth_token(auth_header)
        if not self.check_user_in_db(decode_result):
            return "User not found. Kindly register"
        if not self.is_token_blacklisted(auth_header):
            return "You are logged out, Kindly login again"
        return decode_result

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=3, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def decode_auth_token(self, auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        # import pdb;pdb.set_trace()
        try:
            payload = jwt.decode(auth_token, app.config['SECRET_KEY'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def is_token_blacklisted(self, token):
        query = "select * from blacklisttoken where token = %s"
        is_token = db.qry(query, (token,), fetch="rowcount")

        if not is_token > 0:
            return True
