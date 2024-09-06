from rest_framework.generics import CreateAPIView

from user.serializers import UserRegisterSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer

