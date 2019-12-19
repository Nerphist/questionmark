from django.db import models

# Create your models here.
from users.models import Teacher
from utils.models import AbstractCreateUpdateModel


class Category(AbstractCreateUpdateModel):
    class Meta(AbstractCreateUpdateModel.Meta):
        db_table = 'categories'

    name = models.CharField(max_length=255, null=False, db_index=True, unique=True)


class SubCategory(AbstractCreateUpdateModel):
    class Meta(AbstractCreateUpdateModel.Meta):
        db_table = 'sub_categories'
        unique_together = [['name', 'category']]

    name = models.CharField(max_length=255, null=False, db_index=True)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE, related_name='sub_categories')


class Test(AbstractCreateUpdateModel):
    class Meta(AbstractCreateUpdateModel.Meta):
        db_table = 'tests'

    name = models.CharField(max_length=255, null=False, db_index=True, unique=True)
    information = models.TextField(null=False, blank=True)
    creator = models.ForeignKey(Teacher, null=True, on_delete=models.SET_NULL, related_name='tests')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='tests')


class Question(AbstractCreateUpdateModel):
    class Meta(AbstractCreateUpdateModel.Meta):
        db_table = 'questions'
        unique_together = [['category', 'name']]

    name = models.CharField(max_length=255, null=False)
    text = models.TextField(blank=True)
    test = models.ForeignKey(Test, null=False, on_delete=models.CASCADE, related_name='questions')
    category = models.ForeignKey(SubCategory, null=True, on_delete=models.SET_NULL, related_name='questions')


class Answer(AbstractCreateUpdateModel):
    class Meta(AbstractCreateUpdateModel.Meta):
        db_table = 'answers'
        unique_together = [['question', 'text']]

    text = models.TextField(null=False)
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE, related_name='answers')
    is_right = models.BooleanField(default=False)
