from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models, transaction

# Create your models here.
from utils.models import AbstractCreateUpdateModel


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, AbstractCreateUpdateModel):
    class Meta(AbstractCreateUpdateModel.Meta):
        db_table = 'users'

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=64, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def is_teacher(self):
        try:
            return bool(self.teacher)
        except Teacher.DoesNotExist:
            return False

    def is_assistant(self):
        try:
            return bool(self.assistant)
        except Assistant.DoesNotExist:
            return False

    def is_student(self):
        try:
            return bool(self.student)
        except Student.DoesNotExist:
            return False


class Teacher(AbstractCreateUpdateModel):
    class Meta(AbstractCreateUpdateModel.Meta):
        db_table = 'teachers'

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, unique=True, related_name='teacher')


class Assistant(AbstractCreateUpdateModel):
    class Meta(AbstractCreateUpdateModel.Meta):
        db_table = 'assistants'

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, unique=True, related_name='assistant')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=False, related_name='assistants')


class Student(AbstractCreateUpdateModel):
    class Meta(AbstractCreateUpdateModel.Meta):
        db_table = 'students'

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, unique=True, related_name='student')
