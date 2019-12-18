from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User, Role


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value: str) -> str:
        return make_password(value)

    def validate_role(self, value: Role) -> Role:
        if value.id in (1, 2, 3):
            return value
        else:
            raise ValueError('Role must be in range of 1,2,3')
