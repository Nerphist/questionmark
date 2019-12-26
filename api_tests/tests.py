import inspect

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api_tests.models import *


class TestApiTest(APITestCase):

    def setUp(self) -> None:
        self.category = {
            'name': 'Main category',
        }
        self.sub_category = {
            'name': 'Sub category',
            'category': 'Main category',
        }
        self.test = {
            'name': 'Main test',
            'information': 'Pass this test',
            'category': 'Main category'
        }
        self.question = {
            'name': 'First question',
            'text': 'Who is this?',
            'category': 'toBeUpdated',
            'test': 'toBeUpdated',
        }
        self.question_no_cat = {
            'name': 'Second question',
            'text': 'Who is this?',
            'test': 'toBeUpdated',
        }
        self.answers = [{
            'is_right': i == 2,
            'text': 'Answer %s' % i,
            'question': 'toBeUpdated',
            'position': i, }
            for i in range(1, 5)]
        data = {
            'first_name': 'name',
            'last_name': 'name',
            'email': 'email@mail.com',
            'password': '1111',
        }
        self.client.post(
            path=reverse('teachers'),
            data={
                'user': data,
            },
            format='json'
        )
        response = self.client.post(
            path=reverse('login'),
            data={
                'email': data.get('email'),
                'password': data.get('password')
            },
            format='json'
        )
        self.access = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % self.access)

    def test_create_category(self):
        response = self.client.post(
            path=reverse('categories'),
            data=self.category,
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.first() is not None

    def test_create_test(self):
        self.test_create_category()
        response = self.client.post(
            path=reverse('tests'),
            data=self.test,
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        test = Test.objects.first()
        assert test is not None
        return test

    def test_create_sub_category(self):
        if inspect.stack()[1].function != 'test_create_question':
            self.test_create_category()
        response = self.client.post(
            path=reverse('sub-categories'),
            data=self.sub_category,
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        sub_cat = SubCategory.objects.first()
        assert sub_cat is not None
        return sub_cat

    def test_create_question(self):
        test = self.test_create_test()
        sub_cat = self.test_create_sub_category()
        self.question['test'] = test.id
        self.question['category'] = sub_cat.id
        self.question_no_cat['test'] = test.id
        response = self.client.post(
            path=reverse('questions'),
            data=self.question,
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        question = Question.objects.first()
        assert question is not None
        assert question.category is not None

        response = self.client.post(
            path=reverse('questions'),
            data=self.question_no_cat,
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        question_no_cat = Question.objects.filter(name=self.question_no_cat.get('name')).first()
        assert question_no_cat is not None
        assert question_no_cat.category is None

        return question

    def test_create_answers(self):
        question = self.test_create_question()
        response = None
        for answer in self.answers:
            answer['question'] = question.id
            response = self.client.post(
                path=reverse('answers'),
                data=answer,
                format='json'
            )
            assert response.status_code == status.HTTP_201_CREATED
        assert len(Answer.objects.all()) == len(self.answers)
        assert response is not None
        return response.data

    def test_update_answer(self):
        response = self.test_create_answers()
        answer = self.answers[-1]
        answer['position'] = 1
        pk = response.get('id')
        response = self.client.put(
            path=reverse('answer by id', kwargs={'pk': pk}),
            data=answer,
            format='json'
        )
        print(*Answer.objects.all())
        print(pk)
        assert Answer.objects.get(id=pk).position == 1
        assert len(set(a.position for a in Answer.objects.filter(question_id=answer['question']).all())) == len(
            self.answers)
        assert response.status_code == status.HTTP_200_OK
