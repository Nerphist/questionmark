from django.test import TestCase


# Create your tests here.
class AnalyticsTest(TestCase):
    def setUp(self):
        self.username = 'usuario'
        self.password = 'contrasegna'
        self.data = {
            'username': self.username,
            'password': self.password
        }


