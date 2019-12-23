from functools import reduce

from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api_tests.serializers import *
from users.models import User
from utils.permissions import IsTeacherPost, IsAssistantOrTeacherPostPutDelete, allow_test_modification


class TestView(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    permission_classes = (IsAuthenticated, IsTeacherPost)
    serializer_class = TestSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data['creator'] = request.user.teacher.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request: Request, *args, **kwargs):
        tests = Test.objects
        filters = []
        params = request.query_params
        if params.get('individual'):
            if request.user.is_teacher():
                filters.append(Q(creator_id=request.user.teacher.id))
            elif request.user.is_assistant():
                filters.append(Q(creator_id=request.user.assistant.teacher.id))
            else:
                tests = request.user.student.tests
        if params.get('teacher_id'):
            filters.append(Q(creator_id=params.get('teacher_id')))
        if params.get('category_id'):
            filters.append(Q(category_id=params.get('category_id')))
        elif params.get('category_name'):
            filters.append(Q(category__name=params.get('category_name')))
        if filters:
            tests = tests.filter(reduce(lambda x, y: x & y, filters))
        tests = [TestSerializer(test).data for test in tests.all()]
        return Response(data=tests, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if not allow_test_modification(request.user, Test.objects.get(id=request.data.get('id'))):
            return Response(data={'detail': 'Only teacher and his assistants can create'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, args, kwargs)


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, IsTeacherPost)


class SubCategoryView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsTeacherPost)
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def list(self, request: Request, *args, **kwargs):
        sub_categories = SubCategory.objects
        filters = []
        params = request.query_params
        if params.get('category_name'):
            filters.append(Q(category__name=params.get('category_name')))
        if params.get('category_id'):
            filters.append(Q(category_id=params.get('category_id')))
        if filters:
            sub_categories = sub_categories.filter(reduce(lambda x, y: x & y, filters))
        sub_categories = [SubCategorySerializer(sub_cat).data for sub_cat in sub_categories.all()]
        return Response(data=sub_categories, status=status.HTTP_200_OK)


class QuestionView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAssistantOrTeacherPostPutDelete)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        if not allow_test_modification(request.user, Test.objects.get(id=request.data.get('test'))):
            return Response(data={'detail': 'Only teacher and his assistants can create'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        if not allow_test_modification(request.user, Test.objects.get(id=request.data.get('test'))):
            return Response(data={'detail': 'Only teacher and his assistants can update'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, args, kwargs)

    def list(self, request: Request, *args, **kwargs):
        questions = Question.objects
        filters = []
        params = request.query_params
        if params.get('test_id'):
            filters.append(Q(test_id=params.get('test_id')))
        if params.get('sub_category_id'):
            filters.append(Q(category_id=params.get('sub_category_id')))
        if filters:
            questions = questions.filter(reduce(lambda x, y: x & y, filters))
        questions = [QuestionSerializer(question).data for question in questions.all()]
        return Response(data=questions, status=status.HTTP_200_OK)


class AnswerView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAssistantOrTeacherPostPutDelete)
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def list(self, request, *args, **kwargs):
        answers = Answer.objects
        filters = []
        params = request.query_params
        if params.get('question_id'):
            filters.append(Q(question_id=params.get('question_id')))
        if filters:
            answers = answers.filter(reduce(lambda x, y: x & y, filters))
        answers = [AnswerSerializer(answer).data for answer in answers.all()]
        return Response(data=answers, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not allow_test_modification(request.user, Test.objects.get(
                id=Question.objects.get(id=request.data.get('question')).test_id)):
            return Response(data={'detail': 'Only teacher and his assistants can create'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        if not allow_test_modification(request.user, Test.objects.get(
                id=Question.objects.get(id=request.data.get('question')).test_id)):
            return Response(data={'detail': 'Only teacher and his assistants can update'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, args, kwargs)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated, IsAssistantOrTeacherPostPutDelete])
def allow_test(request: Request, *args, **kwargs):
    data = request.data
    user = User.objects.filter(email=data.get('email')).first()
    test = Test.objects.filter(id=data.get('test_id')).first()
    if not user or not test:
        return Response(data={'detail': 'Some of the resources do not exist'}, status=status.HTTP_400_BAD_REQUEST)
    if not user.is_student():
        return Response(data={'detail': 'The user is not a student'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        try:
            StudentTest.objects.create(student=user.student, test_id=data.get('test_id'))
        except Exception as e:
            return Response({'detail': str(e)}, status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        try:
            StudentTest.objects.get(student=user.student, test_id=data.get('test_id')).delete()
        except Exception as e:
            return Response({'detail': str(e)}, status.HTTP_400_BAD_REQUEST)
    return Response(data={'result': 'success'}, status=status.HTTP_201_CREATED)
