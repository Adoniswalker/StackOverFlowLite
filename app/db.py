"""This file is used to setup and execute database commands"""
# !/usr/bin/env python3
import psycopg2
import psycopg2.extras
from flask import g

from app import app
from config import BaseConfig

configs = BaseConfig()


class DatabaseConfig:
    def create_all(self):
        with app.app_context():
            with app.open_resource('../ddl.sql', mode='r') as f:
                self.qry(f.read(), commit=True)

    def drop_all(self):
        with app.app_context():
            self.qry("drop TABLE answers; drop TABLE questions; drop TABLE users; drop TABLE blacklisttoken", commit=True)

    def connect_db(self):
        """
        This will initialise connection
        :return:
        """
        return psycopg2.connect(configs.DATABASE_URI)

    @app.teardown_appcontext
    def close_db(errors=None):
        """Closes the database again at the end of the request
        if user is not logged in."""
        if hasattr(g, 'db_conn') and not hasattr(g, 'user'):
            print("***CLOSING CONNECTION***")
            g.db_conn.close()
            g.pop('db_conn', None)

    def get_db(self):
        """Opens a new database connection if there is none yet for the
        current application context.
        """
        if not hasattr(g, 'db_conn'):
            g.db_conn = self.connect_db()
        return g.db_conn

    def qry(self, query="", args=(), **kwargs):
        """
        This function is used to execute data queries and return data if needed
        :param query:
        :param args:
        :param kwargs:
        :return:
        """
        conn = self.get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, args)
        if "commit" in kwargs and kwargs["commit"]:
            conn.commit()
        if "fetch" in kwargs and kwargs["fetch"] == "rowcount":
            return cursor.rowcount
        if "fetch" in kwargs and kwargs["fetch"] == "all":
            records = cursor.fetchall()
            return records
        if "fetch" in kwargs and kwargs["fetch"] == "one":
            record = cursor.fetchone()
            if "attr" in kwargs:
                return record[kwargs["attr"]]
            return record
