from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from analytics.models import SolvedTest
from api_tests.models import Test, StudentTest
from api_tests.tests import TestApiTest, Student


class AnalyticsTest(APITestCase):
    def setUp(self) -> None:
        test = TestApiTest()
        test.client = APIClient()
        test.setUp()
        self.test_api = test
        self.data = {
            'first_name': 'name1',
            'last_name': 'name2',
            'email': 'email2@mail.com',
            'password': '1111',
        }
        self.client.post(
            path=reverse('students'),
            data={
                'user': self.data,
            },
            format='json'
        )
        response = self.client.post(
            path=reverse('login'),
            data={
                'email': self.data.get('email'),
                'password': self.data.get('password')
            },
            format='json'
        )
        self.access = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % self.access)

    def test_allow_test(self):
        self.test_api.test_create_answers()
        response = self.test_api.client.post(
            path=reverse('allow_test'),
            data={
                'test': Test.objects.first().id,
                'student': self.data['email']
            },
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        return response.data.get('id')

    def test_start_test(self):
        test_id = self.test_allow_test()
        response = self.client.post(
            path=reverse('solved tests'),
            data={
                'test': StudentTest.objects.get(id=test_id).test.id,
            },
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        self.test_id = response.data.get('id')

    def test_start_questions(self):
        self.test_start_test()
        response = self.client.post(
            path=reverse('solved questions'),
            data={
                'solved_test': self.test_id,
                'question': self.test_api.question['id']
            },
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        return response.data.get('id')

    def test_answer_questions(self):
        question_id = self.test_start_questions()
        for answer in filter(lambda x:x['is_right'], self.test_api.answers):
            response = self.client.post(
                path=reverse('solved answers'),
                data={
                    'solved_question': question_id,
                    'answer': answer['id']
                },
                format='json'
            )
            assert response.status_code == status.HTTP_201_CREATED

    def test_finish_test(self):
        self.test_answer_questions()
        response = self.client.post(
            path=reverse('finish test'),
            data={
                'solved_test': self.test_id,
            },
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK

        response = self.client.post(
            path=reverse('finish test'),
            data={
                'solved_test': self.test_id,
            },
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
