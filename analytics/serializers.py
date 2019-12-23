from rest_framework import serializers

from analytics.models import *
from users.serializers import StudentSerializer


class SolvedTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolvedTest
        fields = ['id', 'test', 'student', 'mark']
        read_only_fields = ['student', 'mark']

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user.student
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
        return super().validate(attrs)


class SolvedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolvedAnswer
        fields = ['id', 'solved_question', 'answer']
