from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

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


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStudent])
def finish_test(request: Request, *args, **kwargs):
    data = request.data
    test = SolvedTest.objects.filter(id=data.get('solved_test')).first()
    if test in request.user.student.solved_tests.all():
        if test.is_checked:
            return Response(data={'detail': 'This test is already checked'}, status=status.HTTP_400_BAD_REQUEST)
        test.check_test()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(data={'detail': 'This test is not for this student'}, status=status.HTTP_403_FORBIDDEN)
