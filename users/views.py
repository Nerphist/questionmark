from uuid import UUID

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api_tests.models import AnonymousLink, StudentTest
from users.models import User, Student, Teacher, Assistant
from users.serializers import StudentSerializer, TeacherSerializer, AssistantSerializer, UserSerializer
from utils.permissions import IsAssistantOrTeacherPostPutDelete


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
    data = request.data
    uid = data.get('uuid')
    serializer = UserSerializer(data={'email': uid + '@anonmail.com', 'password': uid, 'first_name': 'Anonymous',
                                      'last_name': 'Anonymous'})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.get(email=uid + '@anonmail.com')
    student = Student.objects.create(user=user)

    link = AnonymousLink.objects.get(uuid_token=UUID(uid))
    StudentTest.objects.create(test=link.test, student=student)
    link.delete()
    refresh = RefreshToken.for_user(user)
    data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
    print(refresh)
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAssistantOrTeacherPostPutDelete])
def generate_link(request: Request, *args, **kwargs):
    data = request.data
    test_id = data.get('test')
    link = AnonymousLink.objects.create(test_id=test_id)
    uid = link.uuid_token.hex
    return Response(data={'uuid': uid}, status=status.HTTP_200_OK)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request: Request, *args, **kwargs):
    ser = UserSerializer(request.user)
    return Response(ser.data)
