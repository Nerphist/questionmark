from django.urls import path

from api_tests.views import *

urlpatterns = [
    path('tests/', TestView.as_view({
        'post': 'create',
        'get': 'list',
    }), name='tests'),
    path('tests/<int:pk>/', TestView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='test by id'),
    path('categories/', CategoryView.as_view({
        'post': 'create',
        'get': 'list',
    }), name='categories'),
    path('categories/<int:pk>/', CategoryView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='category by id'),
    path('sub-categories/', SubCategoryView.as_view({
        'post': 'create',
        'get': 'list',
    }), name='sub-categories'),
    path('sub-categories/<int:pk>/', SubCategoryView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='subcategory by id'),
    path('questions/', QuestionView.as_view({
        'post': 'create',
        'get': 'list',
    }), name='questions'),
    path('questions/<int:pk>/', QuestionView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='question by id'),
    path('answers/', AnswerView.as_view({
        'post': 'create',
        'get': 'list',
    }), name='answers'),
    path('answers/<int:pk>/', AnswerView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='answer by id'),
    path('allow-test/', allow_test, name='allow_test'),
]
