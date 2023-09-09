from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from accounts.api.serializers import UserSerializer

from tests.data.users import simple_user_data
from tests.helpers.users import create_simple_user


class SetUpTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("user-list")
        return super().setUp()

    def authenticate_client(self, user):
        self.client.force_authenticate(user=user)

    def authenticate_simple_user(self):
        self.user = create_simple_user()
        self.authenticate_client(self.user)


class TestUserListEndpoint(SetUpTestCase):

    def test_create_user(self):
        response = self.client.post(self.url, data=simple_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = UserSerializer(User.objects.get(pk=response.data["id"]))
        self.assertEqual(response.data, serializer.data)

    def test_list_users(self):
        self.authenticate_simple_user()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(User.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)