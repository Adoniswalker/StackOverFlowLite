"""This file is used to setup and execute database commands"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from urllib import parse

import psycopg2
import psycopg2.extras
from flask import g

from app import app


def load_row(row):
    """
    Change the data format
    :param row:
    :return: list
    """
    loaded = {}
    for k, v in row.items():
        loaded[k] = json.loads(v) if isinstance(str, v) else v
    return loaded


def connect_db():
    """
    This will initialise connection
    :return:
    """
    parse.uses_netloc.append("postgres")
    if "DATABASE_URL" in os.environ:
        url = parse.urlparse(os.environ["DATABASE_URL"])
    else:
        url = parse.urlparse(app.config["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    print("***OPENING CONNECTION***")
    return conn


@app.teardown_appcontext
def close_db(errors=None):
    """Closes the database again at the end of the request
    if user is not logged in."""
    if hasattr(g, 'db_conn') and not hasattr(g, 'user'):
        print("***CLOSING CONNECTION***")
        g.db_conn.close()
        g.pop('db_conn', None)


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db_conn'):
        g.db_conn = connect_db()
    return g.db_conn


def qry(query="", args=(), **kwargs):
    """
    This function is used to execute data queries and return data if needed
    :param query:
    :param args:
    :param kwargs:
    :return:
    """
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(query, args)
    if "commit" in kwargs and kwargs["commit"]:
        conn.commit()
    if "fetch" in kwargs and kwargs["fetch"] == "rowcount":
        return cursor.rowcount
    if "fetch" in kwargs and kwargs["fetch"] == "all":
        records = cursor.fetchall()
        if "load" in kwargs and kwargs["load"]:
            loaded_records = []
            for row in records:
                loaded_records.append(load_row(row))
            return loaded_records
        return records
    if "fetch" in kwargs and kwargs["fetch"] == "one":
        record = cursor.fetchone()
        if "load" in kwargs and kwargs["load"]:
            record = load_row(record)
        if "attr" in kwargs:
            return record[kwargs["attr"]]
        return record
