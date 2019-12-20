from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_tests.serializers import *
from utils.permissions import IsTeacher, IsAssistantOrTeacher


class TestView(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = TestSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data['creator'] = request.user.teacher.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, IsTeacher)


class SubCategoryView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAssistantOrTeacher)
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class QuestionView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAssistantOrTeacher)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAssistantOrTeacher)
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
