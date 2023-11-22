from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.response import Response

from accounts.utils import create_test_user


class TestSimpleJWTEndpoint(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_test_user()
        return super().setUp()

    def get_token_pair(self) -> Response:
        return self.client.post(
            reverse("token-pair"),
            data={"username": "test-user", "password": "test#pass"},
        )

    def test_get_token_pair(self):
        response = self.get_token_pair()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_refresh_token(self):
        token_pair_response = self.get_token_pair()
        self.assertIn("refresh", token_pair_response.data)
        refresh_token = token_pair_response.data["refresh"]
        response = self.client.post(
            reverse("token-refresh"), data={"refresh": refresh_token}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
