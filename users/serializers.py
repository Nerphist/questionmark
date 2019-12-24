from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User, Student, Teacher, Assistant


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value: str) -> str:
        return make_password(value)


class FromUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    def create(self, validated_data: dict):
        user = validated_data.pop('user')
        user = User.objects.create(**user)
        validated_data['user'] = user
        student = self.Meta.model.objects.create(**validated_data)
        return student


class StudentSerializer(FromUserSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', ]


class TeacherSerializer(FromUserSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'user', ]


class AssistantSerializer(FromUserSerializer):
    class Meta:
        model = Assistant
        fields = ['id', 'user', 'teacher', ]

    def to_internal_value(self, data):
        data.update({'teacher': self.context['request'].user.teacher.id})
        return super().to_internal_value(data)
