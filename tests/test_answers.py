import json

from basement import TestStackBase


class TestAnswers(TestStackBase):
    def test_post_answer(self):
        """
        Test when posting an answer
        """
        response = self.client_app.post("/api/v1/questions/{}/answers/".format(self.question_id),
                                        data=json.dumps(dict(answer="I prefer with ram")),
                                        content_type="application/json",
                                        headers={'Authorization': self.token})
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertTrue(response_msg['answer'] == 'I prefer with ram')
        assert response.status_code == 201

    def test_post_no_answer(self):
        """
        Testing a question without an answer
        """
        response = self.client_app.post("/api/v1/questions/{}/answers/".format(self.question_id),
                                        data=json.dumps(dict()),
                                        content_type="application/json",
                                        headers={'Authorization': self.token})
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertTrue(response_msg['message']['answer'] ==
                        'Missing required parameter in the JSON '
                        'body or the post body or the query string')
        assert response.status_code == 400

