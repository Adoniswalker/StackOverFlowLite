# StackOverflow-lite
## Introduction
StackOverflow-lite is a platform where people can ask questions and provide answers

[![Build Status](https://travis-ci.org/Adoniswalker/StackOverFlowLite.svg?branch=Chore-add-travis-badge-159859927)](https://travis-ci.org/Adoniswalker/StackOverFlowLite)

[![Coverage Status](https://coveralls.io/repos/github/Adoniswalker/StackOverFlowLite/badge.svg?branch=feature)](https://coveralls.io/github/Adoniswalker/StackOverFlowLite?branch=faeture)

[![Maintainability](https://api.codeclimate.com/v1/badges/d07ddb81fb71a109b9ed/maintainability)](https://codeclimate.com/github/Adoniswalker/StackOverFlowLite/maintainability)
### Features
1. Users can post questions.
2. Users can post answers.
3. Users can view a question with answers to questions.
4. Users can view all the answers

### Installing
Clone the repository [```here```](https://github.com/adoniswalker/StackOverflowlite/)

### Testing
*To test the UI:*\
Navigate to the UI directory
On your preferred browser, open index.html

*To test the API:*\
Navigate to the API/ directory
In a virtual environment, perform the following:

>git checkout feature\
>pip install -r requirements.txt\
>pytest tests/\
>python run.py

*API HOSTED*\
Api are hosted here\
https://stack-overflowlite.herokuapp.com

*Pivotal link*\
https://www.pivotaltracker.com/n/projects/2189449

##Available endpoints
* #### User registration.
    `POST /api/v1/auth/signup/`: 
    ```
    headers = {content_type:application/json}

    {
        "first_name": "John",
        "last_name" : "Doe",
        "email" : "johndoe@gmail.com",
        "password" : "testpassword"

    }
    ```

* #### User login.
    `POST /api/v1/auth/login/`: 
    ```
    headers = {content_type:application/json}

    {
        "username" : "Johnny",
        "password" : "johndoe1234"
    }
    ```

* #### Get all questions.
    `GET /api/v1/questions/`
    ```
    headers = {content_type:application/json}
    ```


* #### Get a question.   
    `GET /api/v1/questions/<questionId>/` 
    ```
    headers = {content_type:application/json} 
    ```
    
* #### Post a question.
    `POST /api/v1/questions/`: 
    ```
    headers = {content_type:application/json, Authorisation:Token <key>}

    {
        "question_subject": "Sample Title",
        "question_body" : "This is a sample description"

    }
    ```

* #### Delete a question.
    `DELETE /api/v1/questions/<questionId>/`:
    ```
    headers = {content_type:application/json, Authorisation:Token <key>}

    ```


* #### Post an answer to a question.
    `POST /api/v1/questions/<questionId>/answers/`:
    ```
    headers = {content_type:application/json, Authorisation:Token <key>}

    {
        "answer": "This is the answer body"
    }
    ```
* #### Mark an answer as preferred question.
    `PUT /questions/<question_id>/answers/<answer_id>/`:
    ```
    headers = {content_type:application/json, Authorisation:Token <key>}

    {
        "vote":1
    }
    ```
* #### Update an answer.
    `PUT /questions/<question_id>/answers/<answer_id>/`:
    ```
    headers = {content_type:application/json, Authorisation:Token <key>}

    {
        "answer":"This is an update to an answer"
    }
    ```
