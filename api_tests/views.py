from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api_tests.serializers import *


class TestView(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryView(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class QuestionView(viewsets.ModelViewSet):
    permission_classes = (AllowAny, )
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerView(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
