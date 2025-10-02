from django.urls import path

from apps.users.api_endpoints import (
    UserRegisterAPIView,
    UserLoginAPIView, 
    UserLogoutAPIView,
    GetProfileAPIView
)

app_name = "users"

urlpatterns = [
    path("user-register/", UserRegisterAPIView.as_view(), name="user_register"),
    path("user-login/", UserLoginAPIView.as_view(), name="user-login"),
    path("user-logout/", UserLogoutAPIView.as_view(), name="user-logout"),
    path("user-profile/", GetProfileAPIView.as_view(), name="user-profile"),
]