from json import dumps

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from assets.models import Currency
from assets.api.serializers import CurrencySerializer

from accounts.utils import create_test_admin, create_test_user
from assets.helpers.test_utils import (
    EUR_DATA,
    create_eur,
    create_currency_pair_list,
)


class SetUpTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = create_test_admin()
        self.client.force_authenticate(user=self.admin)
        self.url = reverse("currency-list")


class TestCurrencyList(SetUpTestCase):
    """Tets the currency-list endpoint with admin authentication"""

    def test_create_currency(self):
        repsonse = self.client.post(self.url, data=EUR_DATA)
        self.assertEqual(repsonse.status_code, status.HTTP_201_CREATED)
        serializer = CurrencySerializer(
            Currency.objects.get(pk=repsonse.data["id"])
        )
        self.assertEqual(repsonse.data, serializer.data)

    def test_retrieve_currency_list(self):
        create_currency_pair_list()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CurrencySerializer(Currency.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)


class TestCurrencyListPermissions(SetUpTestCase):
    """Test the permissions that a non-admin user has over the endpoint"""

    def setUp(self) -> None:
        self.client = APIClient()
        simple_user = create_test_user()
        self.client.force_authenticate(user=simple_user)
        self.url = reverse("currency-list")

    def test_create_currency(self):
        """Non admin users cannot create currencies"""
        repsonse = self.client.post(self.url, data=EUR_DATA)
        self.assertEqual(repsonse.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_currency_list(self):
        """Authenticated users can retrive the list of currencies"""
        create_currency_pair_list()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CurrencySerializer(Currency.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)


class TestCurrencyDetail(TestCase):
    """Tets the currency-detail endpoint with admin authentication"""

    def setUp(self) -> None:
        admin = create_test_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=admin)
        self.currency = create_eur()
        self.url = reverse("currency-detail", kwargs={"pk": self.currency.pk})

    def test_retrieve_currency(self):
        repsonse = self.client.get(self.url)
        self.assertEqual(repsonse.status_code, status.HTTP_200_OK)
        serializer = CurrencySerializer(
            Currency.objects.get(pk=repsonse.data["id"])
        )
        self.assertEqual(repsonse.data, serializer.data)

    def test_update_currency(self):
        response = self.client.patch(
            self.url,
            content_type="application/json",
            data=dumps({"name": "New name"}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CurrencySerializer(
            Currency.objects.get(pk=self.currency.pk)
        )
        self.assertEqual(response.data, serializer.data)

    def test_delete_currency(self):
        """This test is able to pass because the currency to be deleted
        is not related to any CurrencyPair intance."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestCurrencyDetailPermissions(TestCase):
    """Test the permissions that a non-admin user has over the endpoint"""

    def setUp(self) -> None:
        simple_user = create_test_user()
        self.client = APIClient()
        self.client.force_authenticate(user=simple_user)
        self.currency = create_eur()
        self.url = reverse("currency-detail", kwargs={"pk": self.currency.pk})

    def test_retrieve_currency(self):
        repsonse = self.client.get(self.url)
        self.assertEqual(repsonse.status_code, status.HTTP_200_OK)
        serializer = CurrencySerializer(
            Currency.objects.get(pk=repsonse.data["id"])
        )
        self.assertEqual(repsonse.data, serializer.data)

    def test_update_currency(self):
        response = self.client.patch(
            self.url,
            content_type="application/json",
            data=dumps({"name": "New name"}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_currency(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
