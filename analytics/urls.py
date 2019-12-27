from django.urls import path
from analytics.views import *

urlpatterns = [
    path('solved-tests/', SolvedTestView.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
    }), name='solved tests'),
    path('solved-questions/', SolvedQuestionView.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
    }), name='solved questions'),
    path('solved-answers/', SolvedAnswerView.as_view({
        'get': 'list',
        'post': 'create',
    }), name='solved answers'),
    path('solved-tests/<int:pk>/', SolvedTestView.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    }), name='solved tests id'),
    path('solved-questions/<int:pk>/', SolvedQuestionView.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    }), name='solved questions id'),
    path('solved-answers/<int:pk>/', SolvedAnswerView.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    }), name='solved answers id'),
    path('finish-test', finish_test, name='finish test'),
]
