from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import UserRegisterView, UserLoginView

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='user-register'),
    path('refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('login', UserLoginView.as_view(), name='user-login')
]
