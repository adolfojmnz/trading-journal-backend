from django.utils import timezone

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from operations.models import ForexOperation
from operations.api.serializers import ForexOperationSerializer

from tests.helpers.users import create_simple_user
from db.utils import (
    create_eurgbp_pair,
    create_trading_account,
    create_forex_operations,
)


class SetUpMixin(TestCase):

    def setUp(self) -> None:
        self.url = reverse("forex-operation-list")
        self.authenticate_simple_user_client()
        self.trading_account = create_trading_account(user=self.simple_user)

    def authenticate_simple_user_client(self):
        self.client = APIClient()
        self.simple_user = create_simple_user()
        self.client.force_authenticate(user=self.simple_user)


class TestForexOperationListEndpoint(SetUpMixin):

    def test_create_operation(self):
        response = self.client.post(
            self.url,
            data={
                "name": "EUR/GBP Currency Pair",
                "trading_account": self.trading_account.pk,
                "currency_pair": create_eurgbp_pair().pk,
                "status": "PR",
                "position": "SH",
                "open_price": 0.86234,
                "close_price": 0.86539,
                "open_datetime": timezone.now()-timezone.timedelta(hours=2),
                "close_time": timezone.now(),
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = ForexOperationSerializer(
            ForexOperation.objects.get(pk=response.data["id"])
        )
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_operation_list(self):
        create_forex_operations(self.trading_account)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ForexOperationSerializer(
            ForexOperation.objects.all(), many=True
        )
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(ForexOperation.objects.count() > 0)