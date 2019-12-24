from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthViewsTests(APITestCase):

    def setUp(self):
        self.student = {
            'first_name': 'student',
            'last_name': 'student',
            'email': 'student@mail.com',
            'password': '1111',
        }
        self.teacher = {
            'first_name': 'teacher',
            'last_name': 'teacher',
            'email': 'teacher@mail.com',
            'password': '1111',
        }
        self.assistant = {
            'first_name': 'assistant',
            'last_name': 'assistant',
            'email': 'assistant@mail.com',
            'password': '1111',
        }

    def test_register_student(self):
        url = reverse('students')
        response = self.client.post(path=url, data={
            'user': self.student
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_register_teacher(self):
        url = reverse('teachers')
        response = self.client.post(path=url, data={
            'user': self.teacher
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_login(self):
        self.test_register_teacher()
        url = reverse('login')
        response = self.client.post(path=url, data={
            'email': self.teacher.get('email'),
            'password': self.teacher.get('password'),
        }, format='json')
        assert response.status_code == status.HTTP_200_OK
        return response.data.get('access')

    def test_register_assistant(self):
        access = self.test_login()
        url = reverse('assistants')
        response = self.client.post(
            path=url, data={
                'user': self.assistant,
            },
            format='json',
            **{'HTTP_AUTHORIZATION': 'Bearer %s' % access}
        )
        assert response.status_code == status.HTTP_201_CREATED
