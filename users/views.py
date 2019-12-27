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
