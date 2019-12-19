from django.urls import path

from api_tests.views import *

urlpatterns = [
    path('tests/', TestView.as_view({
        'post': 'create',
        'put': 'update',
        'get': 'list',
    }), name='tests'),
    path('categories/', CategoryView.as_view({
        'post': 'create',
        'get': 'list',
    }), name='categories'),
    path('sub-categories/', SubCategoryView.as_view({
        'post': 'create',
        'get': 'list',
    }), name='sub-categories'),
    path('questions/', QuestionView.as_view({
        'post': 'create',
        'put': 'update',
        'get': 'list',
    }), name='questions'),
    path('answers/', AnswerView.as_view({
        'post': 'create',
        'put': 'update',
        'get': 'list',
    }), name='answers'),
]
