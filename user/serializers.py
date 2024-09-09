from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from cash.models import Cash


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, write_only=True, help_text='사용자 이름')
    password = serializers.CharField(required=True, write_only=True, help_text='비밀번호')

    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def _get_token(self, user):
        token = RefreshToken.for_user(user)
        return {
            "access_token": str(token.access_token),
            "refresh_token": str(token)
        }

    def validate(self, attrs):
        if User.objects.filter(username=attrs["username"]).exists():
            raise ValidationError({"username": "이미 존재하는 username입니다."})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        Cash.objects.create(user=user, amount=10000)  # 사용자 생성 시 10000원 제공

        return self._get_token(user)


class UserLoginSerializer(UserRegisterSerializer):
    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise ValidationError("해당하는 사용자가 없습니다. username과 password를 확인하여 주십시오.")
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        return self._get_token(user)
