from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from analytics.serializers import *
from utils.permissions import IsStudent


class SolvedTestView(viewsets.ModelViewSet):
    queryset = SolvedTest.objects.all()
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = SolvedTestSerializer


class SolvedQuestionView(viewsets.ModelViewSet):
    queryset = SolvedQuestion.objects.all()
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = SolvedQuestionSerializer


class SolvedAnswerView(viewsets.ModelViewSet):
    queryset = SolvedAnswer.objects.all()
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = SolvedAnswerSerializer
