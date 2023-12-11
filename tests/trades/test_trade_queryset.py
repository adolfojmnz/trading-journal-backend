from json import dumps

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from tests.utils.accounts import (
    get_or_create_test_user,
    get_or_create_test_admin,
)

from tests.utils.trades import create_forex_trade


class TestTradeQuerySet(TestCase):
    """Test that forex operations are only retrievable by their owners"""

    def setUp(self) -> None:
        self.client = APIClient()
        user = get_or_create_test_user()
        admin = get_or_create_test_admin()
        self.client.force_authenticate(user=admin)
        self.operation = create_forex_trade(user)
        self.url = reverse("trade-detail", kwargs={"pk": self.operation.pk})
        return super().setUp()

    def test_retrieve_trade(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_trade(self):
        data = {"type": "S", "pnl": -60}
        response = self.client.patch(
            self.url, data=dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_trade(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
