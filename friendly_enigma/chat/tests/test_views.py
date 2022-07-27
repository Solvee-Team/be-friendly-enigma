from django.urls import reverse
from chat.serializers import MessageSerializer
from rest_framework import status
from rest_framework.test import (
    APITestCase,
    APIClient,
    force_authenticate,
    APIRequestFactory,
)
from model_bakery import baker

from chat.models import Dialog, Message
from user.models import User
from chat.views import (
    MessageList,
    DialogList,
    UnreadMessagesCountView,
)

factory = APIRequestFactory()
api_client = APIClient()


class TestMessageAndDialogList(APITestCase):
    def setUp(self):
        self.view = MessageList.as_view()
        self.dialog_view = DialogList.as_view()
        self.unread_view = UnreadMessagesCountView.as_view()
        self.first_user = baker.make(User)
        self.second_user = baker.make(User)
        self.member = baker.make(User)
        self.dialog = baker.make(Dialog, users=[self.member, self.first_user])
        self.dialog_2 = baker.make(Dialog, users=[self.member, self.second_user])
        self.message_1 = baker.make(
            Message,
            dialog=self.dialog,
            sender=self.member,
            recipient=self.first_user,
        )
        self.message_2 = baker.make(
            Message,
            dialog=self.dialog,
            sender=self.first_user,
            recipient=self.member,
        )
        self.message_3 = baker.make(
            Message,
            dialog=self.dialog_2,
            sender=self.second_user,
            recipient=self.member,
        )

    def test_get_dialogs(self):
        request = factory.get(reverse("chat:dialogs_list"))
        force_authenticate(request, user=self.member)
        response = self.dialog_view(request)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["unread_count"], 1)

    def test_get_dialogs_after_delete_user(self):
        request = factory.get(reverse("chat:dialogs_list"))
        self.second_user.delete()
        force_authenticate(request, user=self.member)
        response = self.dialog_view(request)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_all_messages(self):
        request = factory.get(reverse("chat:all_messages_list"))
        force_authenticate(request, user=self.member)
        response = self.view(request)
        serializer = MessageSerializer(self.message_3, context={"user": self.member})
        self.assertEqual(len(response.data["results"]), 3)
        self.assertEqual(response.data["results"][0]["pk"], serializer.data["pk"])

    def test_get_messages_by_user_id(self):
        url = reverse(
            "chat:messages_list", kwargs={"user_id": self.second_user.id}
        )
        self.client.force_authenticate(user=self.member)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        serializer = MessageSerializer(self.message_3, context={"user": self.member})
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["pk"], serializer.data["pk"])

    def test_get_unread_count(self):
        request = factory.get(reverse("chat:unread_count"))
        force_authenticate(request, user=self.member)
        response = self.unread_view(request)
        self.assertEqual(response.data["unread_count"], 2)

        force_authenticate(request, user=self.first_user)
        response2 = self.unread_view(request)
        self.assertEqual(response2.data["unread_count"], 1)

    def test_messges_read(self):
        url = reverse(
            "chat:read_messages", kwargs={"user_id": self.second_user.id}
        )
        list_url = reverse("chat:dialogs_list")
        self.client.force_authenticate(user=self.member)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Recheck unread count
        response2 = self.client.get(list_url)
        data = response2.json()
        self.assertEqual(data["results"][0]["unread_count"], 0)
