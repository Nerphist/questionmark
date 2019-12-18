from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

from users.views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', token_obtain_pair, name='login'),
    path('students/', StudentView.as_view({
        'get': 'retrieve',
        'post': 'create',
    }), name='students'),
    path('teachers/', TeacherView.as_view({
        'get': 'retrieve',
        'post': 'create',
    }), name='students'),
    path('assistants/', AssistantView.as_view({
        'get': 'retrieve',
        'post': 'create',
    }), name='students'),
    path('token/refresh/', token_refresh, name='token_refresh'),
    path('checkAuth/', LogoutAPIView.as_view(), name='check')
]
