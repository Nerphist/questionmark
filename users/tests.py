from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Teacher, Student, Assistant


class AuthViewsTest(APITestCase):

    def setUp(self) -> None:
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
        assert Student.objects.filter(user__email=self.student.get('email')).first() is not None

    def test_register_teacher(self):
        url = reverse('teachers')
        response = self.client.post(path=url, data={
            'user': self.teacher
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Teacher.objects.filter(user__email=self.teacher.get('email')).first() is not None

    def test_login(self):
        self.test_register_teacher()
        url = reverse('login')
        response = self.client.post(path=url, data={
            'email': self.teacher.get('email'),
            'password': self.teacher.get('password'),
        }, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        return response.data.get('access')

    def test_register_assistant(self):
        access = self.test_login()
        self.client.credentials(**{'HTTP_AUTHORIZATION': 'Bearer %s' % access})
        url = reverse('assistants')
        response = self.client.post(
            path=url, data={
                'user': self.assistant,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Assistant.objects.filter(user__email=self.assistant.get('email')).first() is not None
