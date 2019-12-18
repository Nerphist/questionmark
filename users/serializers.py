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


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Student
        fields = ['user', ]

    def create(self, validated_data: dict):
        user = validated_data.pop('user')
        user = User.objects.create(**user)
        validated_data['user'] = user
        student = Student.objects.create(**validated_data)
        return student


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        fields = ['user', ]
        model = Teacher

    def create(self, validated_data: dict):
        user = validated_data.pop('user')
        user = User.objects.create(**user)
        validated_data['user'] = user
        teacher = Teacher.objects.create(**validated_data)
        return teacher


class AssistantSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Assistant
        fields = ['user', 'teacher', ]

    def create(self, validated_data: dict):
        user = validated_data.pop('user')
        user = User.objects.create(**user)
        validated_data['user'] = user
        assistant = Assistant.objects.create(**validated_data)
        return assistant
