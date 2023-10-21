from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from accounts.utils import create_test_user

from trades.models import Trade
from trades.serializers import TradeSerializer
from trades.helpers.test_utils import create_forex_trade_list

from assets.helpers.test_utils import create_eurgbp_pair


class TestTradeListEndpoint(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_test_user()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("trade-list")
        return super().setUp()

    def test_create_trade(self):
        response = self.client.post(
            self.url,
            data={
                "user": self.user.pk,
                "ticket": 75824518823,
                "type": "L",
                "currency_pair": create_eurgbp_pair().pk,
                "open_datetime": timezone.now(),
                "close_datetime": timezone.now(),
                "open_price": 1.25467,
                "close_price": 1.25667,
                "stop_loss": 1.25367,
                "take_profit": 1.25666,
                "volume": 0.1,
                "pnl": 20,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = TradeSerializer(
            Trade.objects.get(pk=response.data["id"])
        )
        self.assertEqual(response.data, serializer.data)
        self.tearDown()

    def test_retrieve_trade_list(self):
        create_forex_trade_list(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = TradeSerializer(
            Trade.objects.all(), many=True
        )
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(Trade.objects.count() > 0)
        self.tearDown()