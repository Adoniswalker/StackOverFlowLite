#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import psycopg2
import psycopg2.extras
from flask import g
from urllib import parse

from app import app


def load_row(row):
    loaded = {}
    for k, v in row.items():
        loaded[k] = json.loads(v) if type(v) == str else v
    return loaded


def connect_db():
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
def close_db(error):
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
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(query, args)
    if "commit" in kwargs and kwargs["commit"] == True:
        conn.commit()
    if "fetch" in kwargs and kwargs["fetch"] == "rowcount":
        return cursor.rowcount
    if "fetch" in kwargs and kwargs["fetch"] == "all":
        records = cursor.fetchall()
        if "load" in kwargs and kwargs["load"] == True:
            loaded_records = []
            for row in records:
                loaded_records.append(load_row(row))
            return loaded_records
        return records
    if "fetch" in kwargs and kwargs["fetch"] == "one":
        record = cursor.fetchone()
        if "load" in kwargs and kwargs["load"] == True:
            record = load_row(record)
        if "attr" in kwargs:
            return record[kwargs["attr"]]
        return record
