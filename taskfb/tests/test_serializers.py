from copy import deepcopy

from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from ..models import Interview, Question, Answer, UserAnswer
from django.contrib.auth.models import User


def create_from_json(data):
    interwiev = deepcopy(data)
    question = interwiev.pop('questions')
    Interview.objects.create(**interwiev)
    if question:
        for q in deepcopy(question):
            answers = q.pop('answers')
            inter = Interview.objects.get(pk=interwiev['id'])
            q.pop('interview')
            Question.objects.create(**q, interview=inter)
            if answers:
                for a in answers:
                    que = Question.objects.get(pk=q['id'])
                    a.pop('question')
                    Answer.objects.create(**a, question=que)


class SetUP:

    admin = 'admin'
    password  = 'mypassword'

    @classmethod
    def setClientCredentions(cls, client):
        resp = client.post('/api/login/', data={'username': cls.admin, 'password': cls.password}, format='json')
        token = resp.json()['token']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return client

    @classmethod
    def createSU(cls):
        my_admin = User.objects.create_superuser(cls.admin, 'myemail@test.com', cls.password)
        cls.my_admin = my_admin

class TestInterviewListView1(TestCase, SetUP):
    interview = {
        "id": 2,
        "title": "first",
        # "started_at": None,
        # "ended_at": None,
        "description": "be or not to be",
    }

    @classmethod
    def setUpTestData(cls):
        obj = Interview.objects.create(**cls.interview)

    def test_get1(self):
        request = self.client.get('/api/interview/', )
        data = request.json()[0]
        for k, v in self.interview.items():
            self.assertIn(k, data.keys())
            self.assertIn(v, data.values())
        self.assertIn('started_at', data.keys())
        self.assertIn('ended_at', data.keys())


class TestInterviewListView2(TestCase, SetUP):

    @classmethod
    def setUpTestData(cls):
        cls.createSU()
        cls.client = APIClient()
        # cls.client_auth = cls.setClientCredentions(cls.client)


    test_data_1 = {
        "title": "first",
        "description": "be or not to be",
        "questions": [
            {
                "text": "r2",
                "type_question": "multichoice",
                "answers": [
                    {
                        "text": "gsd",
                    },
                    {
                        "text": "gsd",
                    }
                ],
            },
            {
                "text": "rr1",
                "type_question": "text",
                "answers": [],
            }
        ]
    }
    test_data_1_answ = {'title': 'first', 'started_at': None, 'ended_at': None, 'description': 'be or not to be',
                        'questions': [{'text': 'rr1', 'type_question': 'text', 'answers': []},
                                      {'text': 'r2',
                                       'type_question': 'multichoice',
                                       'answers': [{'text': 'gsd'},
                                                   {'text': 'gsd'}]}]}

    def setUp(self):
        self.client_auth = self.setClientCredentions(APIClient())

    def test_post(self):
        self.client_auth = self.setClientCredentions(self.client)
        request = self.client_auth.post('/api/interview/', data=self.test_data_1, format='json')
        self.assertEquals(201, request.status_code)
        data = request.json()
        self.assertDictEqual(data, self.test_data_1_answ)


class TestInterviewDetailView1(TestCase, SetUP):

    test_data_1 = {
        "id": 3,
        "title": "t2",
        "started_at": '2020-10-16T12:12:35',
        "ended_at": None,
        "description": "ttt2",
        "questions": [
            {
                "id": 3,
                "text": "vopros2",
                "type_question": "text",
                "answers": [
                    {
                        "id": 2,
                        "text": "3444",
                        "question": 3
                    }
                ],
                "interview": 3
            }
        ]
    }

    @classmethod
    def setUpTestData(cls):
        # interwiev = deepcopy(cls.test_data_1)
        cls.createSU()
        create_from_json(cls.test_data_1)

    def test_get(self):
        request = self.client.get('/api/interview/3/', )
        self.assertEquals(200, request.status_code)
        data = request.json()
        pass


    def test_post(self):
        self.client_auth = self.setClientCredentions(self.client)
        test_data = deepcopy(self.test_data_1)
        del test_data['id']
        request = self.client_auth.post('/api/interview/4/', data=test_data, format='json')
        self.assertEquals(200, request.status_code)






