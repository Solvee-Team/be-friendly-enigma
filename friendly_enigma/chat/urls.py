from django.urls import path
from . import consumers
from . import views

app_name = "chat"

urlpatterns = [
    path("messages", views.MessageList.as_view(), name="all_messages_list"),
    path(
        "messages/unread_count",
        views.UnreadMessagesCountView.as_view(),
        name="unread_count",
    ),
    path(
        "messages/<int:user_id>",
        views.MessageList.as_view(),
        name="messages_list",
    ),
    path("dialogs", views.DialogList.as_view(), name="dialogs_list"),
    path("users", views.UsersForMessagesList.as_view(), name="users_list"),
    path(
        "messages/<int:user_id>/read",
        views.ReadMessagesView.as_view(),
        name="read_messages",
    ),
]
