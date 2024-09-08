from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def _get_token(self, user):
        token = RefreshToken.for_user(user)
        return {
            "access_token": str(token.access_token),
            "refresh_token": str(token)
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'])
        user.set_password(validated_data['password'])

        return self._get_token(user)


class UserLoginSerializer(UserRegisterSerializer):

    def create(self, validated_data):
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if not user:
            raise ValidationError("해당 하는 사용자가 없습니다. username과 password를 확인하여 주십시오.")

        return self._get_token(user)
