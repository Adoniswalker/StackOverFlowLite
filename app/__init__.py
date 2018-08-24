"""This file is used to initialise this package and create app,also running the server"""
from flask import Flask


app = Flask(__name__, instance_relative_config=True)

from app import views

app.config.from_object('config')
