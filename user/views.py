from rest_framework.generics import CreateAPIView

from user.serializers import UserRegisterSerializer, UserLoginSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer
