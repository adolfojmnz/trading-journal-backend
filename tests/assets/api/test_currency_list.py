from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from assets.models import Currency
from assets.api.serializers import CurrencySerializer

from tests.helpers.users import create_staff_user, create_simple_user
from tests.helpers.assets.forex.single import (
    create_eur_currency,
    create_gbp_currency,
    create_jpy_currency,
)
from tests.data.assets.forex.single import eur as eur_data


class SetUpTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = create_staff_user()
        self.client.force_authenticate(user=self.admin)
        self.url = reverse("currency-list")

    def create_currency_list(self):
        create_eur_currency()
        create_gbp_currency()
        create_jpy_currency()


class TestCurrencyListEndpoint(SetUpTestCase):
    """ Tets the currency-list endpoint with admin authentication """

    def test_create_currency(self):
        repsonse = self.client.post(self.url, data=eur_data)
        self.assertEqual(repsonse.status_code, status.HTTP_201_CREATED)
        serializer = CurrencySerializer(
            Currency.objects.get(pk=repsonse.data["id"])
        )
        self.assertEqual(repsonse.data, serializer.data)

    def test_retrieve_currency_list(self):
        self.create_currency_list()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CurrencySerializer(Currency.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)


class TestCurrencyListPermissions(SetUpTestCase):
    """ Test the permissions that a non-admin user has over the endpoint """

    def setUp(self) -> None:
        self.client = APIClient()
        simple_user = create_simple_user()
        self.client.force_authenticate(user=simple_user)
        self.url = reverse("currency-list")


    def test_create_currency(self):
        """ Non admin users cannot create currencies """
        repsonse = self.client.post(self.url, data=eur_data)
        self.assertEqual(repsonse.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_currency_list(self):
        """ Authenticated users can retrive the list of currencies """
        self.create_currency_list()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CurrencySerializer(Currency.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)