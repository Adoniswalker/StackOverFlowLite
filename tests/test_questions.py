"""This file is used for testcases"""
import json

import pytest
from app import views


@pytest.fixture
def client():
    """This function is using for setting up test environment"""
    views.app.config['TESTING'] = True
    client = views.app.test_client()
    with views.app.app_context():
        yield client


def test_get_questions(client):
    """Start with a blank database."""
    response = client.get('/api/v1/questions/')
    assert response.is_json is True


def test_post_question(client):
    """
    Tests a user can post a question.
    """
    question = {
        "subject": "What is computer programming?",
        "body": "It is important to note that jobs do not share storage, as each job runs in a "
                "fresh VM or"}

    response = client.post("/api/v1/questions/",
                           data=json.dumps(question),
                           content_type="application/json")
    assert response.status_code == 201


def test_post_question_empty_body(client):
    """
    Tests user cannnot ask a question without body content
    """
    response = client.post("/api/v1/questions/",
                           data=json.dumps(dict(subject="how to delete git branch",
                                                body="")),
                           content_type="application/json")
    assert response.status_code == 400
    response_msg = json.loads(response.data.decode("UTF-8"))
    assert response_msg["Error"] == "Please provide all fields with keys 'subject' and 'body'"


def test_post_question_no_subject(client):
    """
    Check if question can be added without function
    """
    response = client.post("/api/v1/questions/",
                           data=json.dumps(dict(subject="",
                                                body="I want to delete a branch both locally..")),
                           content_type="application/json")
    assert response.status_code == 400
    response_msg = json.loads(response.data.decode("UTF-8"))
    assert response_msg["Error"] == "Please provide all fields with keys 'subject' and 'body'"


def test_get_one_question_by_id(client):
    """
    Tests a user can get a question by id.
    """
    response = client.get("/api/v1/questions/1/")
    assert response.status_code == 200
    response_msg = json.loads(response.data.decode("UTF-8"))
    assert response_msg["subject"] == "What is js?"


def test_get_question_no_id(client):
    """Used to test what code is returned when getting question with no id"""
    response = client.get("/api/v1/questions/1000/")
    assert response.status_code == 404
