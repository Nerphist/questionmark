import threading
import time

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User, Student, Teacher, Assistant
from users.serializers import UserSerializer, StudentSerializer, TeacherSerializer, AssistantSerializer


class StudentView(ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = StudentSerializer


class TeacherView(ModelViewSet):
    queryset = Teacher.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TeacherSerializer


class AssistantView(ModelViewSet):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def anonymous_user(request: Request, *args, **kwargs):
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_role(request: Request, *args, **kwargs):
    if request.user.is_teacher():
        role = 'teacher'
    elif request.user.is_assistant():
        role = 'assistant'
    else:
        role = 'student'
    return Response({'role': role}, status=status.HTTP_200_OK)
