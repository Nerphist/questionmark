from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User, Student, Teacher, Assistant
from users.serializers import UserSerializer, StudentSerializer, TeacherSerializer, AssistantSerializer


class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        user_object = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
    permission_classes = (AllowAny,)
    serializer_class = AssistantSerializer


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
