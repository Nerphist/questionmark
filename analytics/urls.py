from django.urls import path
from analytics.views import *

urlpatterns = [
    path('solved-tests/', SolvedTestView.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
    })),
    path('solved-questions/', SolvedQuestionView.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
    })),
    path('solved-answers/', SolvedAnswerView.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('solved-tests/<int:pk>/', SolvedTestView.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    })),
    path('solved-questions/<int:pk>/', SolvedQuestionView.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    })),
    path('solved-answers/<int:pk>/', SolvedAnswerView.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    })),
]
