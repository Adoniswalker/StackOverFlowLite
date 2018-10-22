"""This module manipulates the different models"""
import psycopg2
import re

from flask import request

from app import app
from app.auth import Authentication
from app.db import DatabaseConfig
from flask_bcrypt import Bcrypt, check_password_hash

db = DatabaseConfig()
b_crypt = Bcrypt(app)
auth = Authentication()


def get_username(first_name, last_name, email):

    if last_name and first_name:
        return first_name + " " + last_name
    else:
        return email.split("@")[0]


class Users:

    def save(self, args):
        """
        Will add new user to database
        :param args:
        :return:
        """
        query = "insert into users (first_name, last_name, email, password_hash)" \
                " values (%s,%s,%s, %s) returning account_id, first_name, last_name,  email"
        arguments = (
            args['first_name'], args['last_name'], args['email'],
            b_crypt.generate_password_hash(args['password']).decode('utf-8'))
        user = db.qry(query, arguments, fetch="one", commit=True)
        user["message"] = "You have succefully signed up"
        return user

    def email_address(self, value, name):
        """
        Will validate an email
        :param value:
        :param name:
        :return:
        """
        is_mail = self.is_email_valid(value, name)
        if not is_mail == value:
            return is_mail
        email_count = db.qry("select email from users where email =%s",
                             (value.strip(),), fetch="rowcount")
        if email_count >= 1:
            raise ValueError("'{}' has already been registered".format(value.strip()))
        return value

    def is_email_valid(self, email, name):
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email.strip()):
            raise ValueError("The parameter '{}' is not a valid email."
                             " You gave us the value:{}".format(name, email))
        return email

    def logout(self, token):
        query = "insert into blacklisttoken (token)values (%s)"
        token = token.split(' ')[-1].strip()
        arguments = (token,)
        try:
            db.qry(query, arguments, commit=True)
        except psycopg2.IntegrityError as e:
            pass
        return {
                   'status': 'success',
                   'message': 'Successfully logged out.'
               }, 200

    def password_valid(self, value, name):
        """
        Validate a password provided
        :param value:
        :param name:
        :return:
        """
        password_regex = r"(?=.{8,})"
        if not re.match(password_regex, value.strip()):
            raise ValueError(
                "The parameter '{}' must be 8 characters or more. "
                "Your password length is:{}".format(name, len(value)))
        return value

    def login(self, args):
        """
        Processs the user login
        :param args:
        :return:
        """
        query = "select account_id, first_name, last_name, email, " \
                "password_hash from users where  email = %s;"
        results = db.qry(query, (args['email'],), fetch="one")
        if not results:
            return {"Error": "Email not registered"}, 404
        elif check_password_hash(results['password_hash'], args['password']):
            results.pop("password_hash")
            auth_token = auth.encode_auth_token(str(results["account_id"])).decode()
            results["auth_token"] = auth_token
            return results, 200
        else:
            return {"Error": "Wrong password"}, 400

    def get_user(self, user_id):
        question = db.qry("select u.account_id, u.first_name, u.last_name,u.email, "
                          "(select count(answer_obj.posted_by) from questions answer_obj where"
                          " answer_obj.posted_by = %s) as questions_counts,"
                          "(select count(a.answeres_by) from answers a where "
                          "a.answeres_by = %s) as answers_counts"
                          " from users u where u.account_id = %s;",
                          (user_id, user_id, user_id,), fetch="one")
        return question, 200
