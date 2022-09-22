from django.urls import path
from .registration_views import RegisterBaseInfoView
from .views import (
    MyUserInfoView, UserUpdatePasswordView,
    DecoratedTokenRefreshView, DeleteAcount, UpdateChatStyle,
    UpdateTheme, UserSearchView
)

app_name = "auth_app"

urlpatterns = [
    path("register/base", RegisterBaseInfoView.as_view(), name="register-base"),
    path("me", MyUserInfoView.as_view(), name="me"),
    path("change-password", UserUpdatePasswordView.as_view(), name="change-password"),
    path("token/refresh", DecoratedTokenRefreshView.as_view(), name="token/refresh"),
    path("delete-acount", DeleteAcount.as_view(), name="delete-acount"),
    path("update-chat-style", UpdateChatStyle.as_view(), name="update-chat-style"),
    path("update-theme", UpdateTheme.as_view(), name="update-theme"),
    path("chat-style-and-theme", UpdateTheme.as_view(), name="chat-style-and-theme"),
    path("user-search", UserSearchView.as_view(), name="get-users"),
]
