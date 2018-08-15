"""This is the class tha represents questions"""


class Questions:
    """Question class to manipulate questions"""

    def __init__(self):
        """This initialises some few questions"""
        self.questions = [
            {'id': 1, 'subject': 'What is js?',
             "body": "Using tools that automate buildand testing when code is committed"
                     " to a version control system",
             'answers': ['Answer one', 'Answer two', 'Answer three']},
            {'id': 2, 'subject': 'Is using APIs good?',
             "body": "Creating API endpoints that will be consumed using Postman",
             'answers': ['Answer one', 'Answer two', 'Answer three']},
            {'id': 3, 'subject': 'What is tdd?', "body": "What is test "
                                                         "driven development,"
                                                         " i come across it yesterday",
             'answers': ['Answer one', 'Answer two', 'Answer three']}]

    def get_all_questions(self):
        """Used to get all questions"""
        questions_list = [{'id': question['id'], 'subject': question['subject'],
                           'body': question['body']} for question in self.questions]
        return questions_list

    def get_one_question(self, question_id):
        """Used to get one question"""
        return [position for position in self.questions if position['id'] == question_id]

    def post_question(self, subject, body):
        """Used to post a question"""
        new_id = max([i['id'] for i in self.questions]) + 1 or 1
        question_dict = {
            'id': new_id,
            'subject': subject,
            'body': body,
            'answers': []
        }
        self.questions.append(question_dict)
        return question_dict

    def post_answer(self, question_id, answer):
        """Used to post an answer"""
        question = [position for position in self.questions if position['id'] == question_id]
        if not question:
            return None
        question[0]['answers'].append(answer)
        return answer