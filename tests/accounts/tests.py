from json import dumps

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from accounts.api.serializers import UserSerializer

from tests.utils.accounts import get_or_create_test_user


class TestUserListEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("user-list")
        return super().setUp()

    def authenticate_client(self):
        self.client.force_authenticate(user=get_or_create_test_user())

    def test_create_user(self):
        response = self.client.post(
            self.url, data={"username": "test-user", "password": "test#pass"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = UserSerializer(User.objects.get(pk=response.data["id"]))
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_user_list(self):
        self.authenticate_client()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(User.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(User.objects.count() > 0)


class TestUserDetailEndpoint(TestCase):
    def setUp(self):
        self.user = get_or_create_test_user()
        self.url = reverse(
            "user-detail",
            kwargs={"pk": self.user.pk},
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    def test_retrieve_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(self.user)
        self.assertEqual(response.data, serializer.data)

    def test_update_user(self):
        response = self.client.patch(
            self.url,
            content_type="application/json",
            data=dumps({"username": "new-username"}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(User.objects.get(pk=self.user.pk))
        self.assertEqual(response.data, serializer.data)

    def test_delete_user(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user.pk).is_active, False)
