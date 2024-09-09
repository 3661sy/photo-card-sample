from rest_framework.generics import CreateAPIView

from user.serializers import UserRegisterSerializer, UserLoginSerializer


class UserRegisterView(CreateAPIView):
    """
    사용자 회원가입 api

    Request Field:
        username: string
        password: string

    Response Field:
        access_token: string
        refresh_token: string

    """
    serializer_class = UserRegisterSerializer


class UserLoginView(CreateAPIView):
    """
    로그인 api

    Request Field:
        username: string
        password: string

    Response Field:
        access_token: string
        refresh_token: string

    """
    serializer_class = UserLoginSerializer
