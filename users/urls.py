from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

from users.views import RegisterAPIView, LogoutAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', token_obtain_pair, name='login'),
    path('api/token/refresh/', token_refresh, name='token_refresh'),
    path('checkAuth/', LogoutAPIView.as_view(), name='check')
]
