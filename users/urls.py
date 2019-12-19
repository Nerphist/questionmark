from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

from users.views import *

urlpatterns = [
    path('login/', token_obtain_pair, name='login'),
    path('students/', StudentView.as_view({
        'post': 'create',
    }), name='students'),
    path('teachers/', TeacherView.as_view({
        'post': 'create',
    }), name='teachers'),
    path('assistants/', AssistantView.as_view({
        'post': 'create',
    }), name='assistants'),
    path('token/refresh/', token_refresh, name='token_refresh'),
    path('checkAuth/', LogoutAPIView.as_view(), name='check')
]
