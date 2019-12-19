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
    class CategorySerializer(SubCategorySerializer):
        class Meta(SubCategorySerializer.Meta):
            validators = []

    category = CategorySerializer()

    class Meta:
        model = Question
        fields = ['id', 'name', 'text', 'category', 'test']

    def validate_category(self, value):
        sub_category = SubCategory.objects.filter(category=value.get('category'), name=value.get('name')).first()
        return sub_category


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
