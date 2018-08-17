class Questions:
    def __init__(self):
        self.questions = [
            {'id': 1, 'subject': 'What is js?',
             "body": "Using tools that automate buildand testing when code is committed to a version control system",
             'answers': ['Answer one', 'Answer two', 'Answer three']},
            {'id': 2, 'subject': 'Is using APIs good?',
             "body": "Creating API endpoints that will be consumed using Postman",
             'answers': ['Answer one', 'Answer two', 'Answer three']},
            {'id': 3, 'subject': 'What is tdd?', "body": "What is test driven development, i come across it yesterday",
             'answers': ['Answer one', 'Answer two', 'Answer three']}]

    def get_all_questions(self):
        questions_list = [{'id': question['id'], 'subject': question['subject'],
                           'body': question['body']} for question in self.questions]
        return questions_list

    def get_one_question(self, questionId):
        return [position for position in self.questions if position['id'] == questionId]
