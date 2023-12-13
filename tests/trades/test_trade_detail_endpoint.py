from json import dumps

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from trades.models import Trade
from trades.api.serializers import TradeSerializer

from tests.utils.accounts import get_or_create_test_user
from tests.utils.trades import create_forex_trade


class TestTradeDetail(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_or_create_test_user()
        self.client.force_authenticate(user=self.user)
        self.trade = create_forex_trade(self.user)
        self.url = reverse("trade-detail", kwargs={"pk": self.trade.pk})
        return super().setUp()

    def test_retrive_trade(self):
        response = self.client.get(self.url)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        serializer = TradeSerializer(Trade.objects.get(pk=response.data["id"]))
        self.assertEqual(response.data, serializer.data)

    def test_update_trade(self):
        data = {"type": "S", "pnl": -60}
        response = self.client.patch(
            self.url, data=dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = TradeSerializer(Trade.objects.get(pk=response.data["id"]))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(serializer.instance.pnl, -60)
        self.assertEqual(serializer.instance.type, "S")

    def test_delete_trade(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
