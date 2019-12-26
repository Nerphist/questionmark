from rest_framework import serializers

from api_tests.models import *


class TestSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Test
        fields = ['id', 'name', 'category', 'information', 'creator']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']


class QuestionSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), required=False, allow_null=True,
                                                  default=None)
    position = serializers.ModelField(Question()._meta.get_field('position'), required=False, allow_null=True,
                                      default=1)

    class Meta:
        model = Question
        fields = ['id', 'name', 'text', 'category', 'test', 'position']


class AnswerSerializer(serializers.ModelSerializer):
    position = serializers.ModelField(Answer()._meta.get_field('position'), required=False, allow_null=True, default=1)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'is_right', 'text', 'position']
