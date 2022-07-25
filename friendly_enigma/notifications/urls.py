from django.urls import path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from . import views
from .handlers import *

app_name = "notifications"


urlpatterns = [
    path("all", views.AllNotificationList.as_view(), name="all_notification_list"),
    path(
        "unread",
        views.UnreadNotificationList.as_view(),
        name="unread_notification_list",
    ),
    path(
        "read",
        views.ReadNotificationsView.as_view(),
        name="read_notification_list",
    ),
    path(
        "unread_count",
        views.UnreadNotificationsCountView.as_view(),
        name="unread_count",
    ),
    path(
        "devices/register",
        FCMDeviceAuthorizedViewSet.as_view({"post": "create"}),
        name="create_fcm_device",
    ),
]
