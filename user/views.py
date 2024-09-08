from rest_framework.generics import CreateAPIView

from user.serializers import UserRegisterSerializer, UserLoginSerializer


class UserRegisterView(CreateAPIView):
    """
    Display an individual

    :param url: 불러올 url

    :template:`myapp/my_template.html`

    """
    serializer_class = UserRegisterSerializer


class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer
