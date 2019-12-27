from rest_framework import serializers

from analytics.models import *
from users.serializers import StudentSerializer


class SolvedTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolvedTest
        fields = ['id', 'test', 'student', 'mark', 'is_checked']
        read_only_fields = ['student', 'mark', 'is_checked']

    def create(self, validated_data):
        student = self.context['request'].user.student
        validated_data['student'] = student
        if validated_data['test'] not in (i.test for i in student.tests.all()):
            raise ValueError('Student is not allowed to try this test')
        data = super().create(validated_data)
        return data


class SolvedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolvedQuestion
        fields = ['id', 'question', 'solved_test', 'correct']
        read_only_fields = ['correct']

    def validate(self, attrs):
        if attrs.get('question') not in attrs.get('solved_test').test.questions.all():
            raise ValueError('This question is not in this test')
        if attrs.get('solved_test').is_checked:
            raise ValueError('Test is already checked')
        return super().validate(attrs)


class SolvedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolvedAnswer
        fields = ['id', 'solved_question', 'answer']

    def validate(self, attrs):
        if attrs.get('solved_question').solved_test.is_checked:
            raise ValueError('Test is already checked')
        return super().validate(attrs)
