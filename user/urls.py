from django.urls import path
from .registration_views import RegisterBaseInfoView
from .views import MyUserInfoView, UserUpdatePasswordView
app_name = "auth_app"

urlpatterns = [
    path("register/base", RegisterBaseInfoView.as_view(), name="register-base"),
    path("me", MyUserInfoView.as_view(), name="me"),
    path("change-password", UserUpdatePasswordView.as_view(), name="change-password"),
]
