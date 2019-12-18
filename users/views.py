from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import AssistantTeacher, User
from users.serializers import UserSerializer


class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        user_object = serializer.save()
        if user_object.role_id == 3:
            if user.get('teacher_email') and isinstance(user.get('teacher_email'), str):
                try:
                    teacher = User.objects.get(email=user['teacher_email'])
                except:
                    return Response({'error': 'no teacher with such email'},
                                    status=status.HTTP_404_NOT_FOUND)
                AssistantTeacher.objects.create(teacher_id=teacher.id, assistant_id=user_object.id)
            else:
                return Response({'error': 'teacher_email field is required for assistant registration'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
