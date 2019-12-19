from django.urls import path

from api_tests.views import *

urlpatterns = [
    path('tests/', TestView.as_view({
        'post': 'create',
    }), name='tests'),
    path('categories/', CategoryView.as_view({
        'post': 'create',
    }), name='categories'),
    path('sub-categories/', SubCategoryView.as_view({
        'post': 'create',
    }), name='sub-categories'),
    path('questions/', QuestionView.as_view({
        'post': 'create',
    }), name='tests'),
    path('answers/', AnswerView.as_view({
        'post': 'create',
    }), name='tests'),
]
