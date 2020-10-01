from copy import deepcopy

from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from ..models import Interview, Question, Answer, UserAnswer
from django.contrib.auth.models import User
from copy import deepcopy

DATA_CASE = {
    "q_interview_1" : {
            "title": "Опрос 1",
            "started_at": "2020-10-16T12:12:35",
            "ended_at": None,
            "description": "тестовый опрос"
    },

    "q_question_1_text" : {
        "text": "vopros1",
        "type_question": "text",

    },

    "q_question_2_choice" : {
        "text": "vopros2",
        "type_question": "choice",

    },

    "q_question_3_multi_choice" : {
        "text": "vopros2",
        "type_question": "multi",
    },


    "q_answer_text_1" : {
        "text": "текстовый ответ",
    },

    "q_answer_text_2" : {
        "text": "текстовый ответ 2",
    },
}


class DataCase():
    q_interview_1 = None
    q_question_1_text = None
    q_question_2_choice = None
    q_question_3_multi_choice = None
    q_answer_text_1 = None
    q_answer_text_2 =None





class Credentions:

    admin = 'admin'
    password = 'mypassword'

    @classmethod
    def set_or_get_auth_client(cls, client=None, n=0):
        if n == 2:
            return client
        if not client:
            client = APIClient()
        resp = client.post('/api/login/', data={'username': cls.admin, 'password': cls.password}, format='json')
        if resp.status_code == 400:
            cls.createSU()
            return cls.set_or_get_auth_client(client=client, n=n+1)
        token = resp.json()['token']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return client

    @classmethod
    def createSU(cls):
        my_admin = User.objects.create_superuser(cls.admin, 'myemail@test.com', cls.password)
        cls.my_admin = my_admin


class TestInterviewListView(DataCase, TestCase):
    auth_client = Credentions.set_or_get_auth_client()

    def setUp(self) -> None:
        for k, v in DATA_CASE.items():
            setattr(self, k, deepcopy(v))

    def test_post_1(self):
        self.auth_client = Credentions.set_or_get_auth_client()
        resp = self.auth_client.post('/api/interview/', data=self.q_interview_1, format='json')
        self.assertEqual(resp.status_code , 201)
        self.q_interview_1['questions'] = [self.q_question_2_choice]
        query = self.q_interview_1
        resp = self.auth_client.post('/api/interview/', data=query, format='json')
        self.assertEqual(resp.status_code, 201)
        self.q_question_2_choice['answers'] = [self.q_answer_text_1, self.q_answer_text_2]
        self.q_question_3_multi_choice['answers'] = [self.q_answer_text_2, self.q_answer_text_1]
        self.q_interview_1['questions'] = [self.q_question_2_choice, self.q_question_1_text, self.q_question_3_multi_choice]
        query = self.q_interview_1
        resp = self.auth_client.post('/api/interview/', data=query, format='json')
        self.assertEqual(resp.status_code, 201)

    def test_put(self):
        self.auth_client = Credentions.set_or_get_auth_client()
        resp = self.auth_client.post('/api/interview/5/', data=self.q_interview_1, format='json')
        self.assertEqual(resp.status_code, 201)
        j = resp.json()
        self.assertEqual(j['id'], 5)
        description = j['description']
        self.q_interview_1['description'] = description + 'test'
        resp = self.auth_client.put('/api/interview/5/', data=self.q_interview_1, format='json')
        self.assertEqual(resp.status_code, 400)
        j = resp.json()
        self.assertIn('field ended', j['error'])
        b'{"error":"field ended_atis Null in db or does not sent."}'
        self.q_interview_1['ended_at'] = '2020-12-1T00:00:01'
        resp = self.auth_client.put('/api/interview/5/', data=self.q_interview_1, format='json')
        self.assertEqual(resp.status_code, 200)
        j = resp.json()
        self.assertEqual(j['id'], 5)
        self.assertEqual(j['description'], description + 'test')

    def test_delete(self):
        self.auth_client = Credentions.set_or_get_auth_client()
        resp = self.auth_client.post('/api/interview/5/', data=self.q_interview_1, format='json')
        self.assertEqual(resp.status_code, 201)
        j = resp.json()
        resp = self.auth_client.delete('/api/interview/5/')
        self.assertEqual(resp.status_code, 400)
        self.q_interview_1['ended_at'] = '2020-12-1T00:00:01'
        resp = self.auth_client.put('/api/interview/5/', data=self.q_interview_1, format='json')
        j = resp.json()
        self.assertEqual(resp.status_code, 200)
        resp = self.auth_client.delete('/api/interview/5/')
        self.assertEqual(resp.status_code, 204)
        i = Interview.objects.filter(pk=j['id'])
        self.assertEqual(0, len(i))
        resp = self.auth_client.get('/api/interview/5/')
        self.assertEqual(resp.status_code, 404)
















