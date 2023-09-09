from json import dumps

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from accounts.api.serializers import UserSerializer

from tests.helpers.users import create_simple_user


class SetUpTestCase(TestCase):

    def setUp(self):
        self.user = create_simple_user()
        self.url = reverse(
            "user-detail", kwargs={"pk": self.user.pk}
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        return super().setUp()


class TestUserListEndpoint(SetUpTestCase):

    def test_retrieve_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.user)
        self.assertEqual(response.data, serializer.data)

    def test_update_user(self):
        response = self.client.patch(self.url,
                                    content_type="application/json",
                                    data=dumps({"username": "new-username"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(User.objects.get(pk=self.user.pk))
        self.assertEqual(response.data, serializer.data)

    def test_destroy_user(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user.pk).is_active, False)