from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from assets.models import CurrencyPair
from assets.api.serializers import CurrencyPairSerializer

from tests.helpers.users import (
    create_staff_user,
    create_simple_user,
)
from tests.helpers.assets.forex.single import (
    create_eur_currency,
    create_gbp_currency,
)
from tests.helpers.assets.forex.pair import (
    create_eur_gbp_pair,
    create_eur_jpy_pair,
    create_gbp_jpy_pair,
)
from tests.data.assets.forex.pair import eur_gbp as eur_gbp_data


class SetUpMixin(TestCase):

    def authenticate_admin_client(self):
        admin = create_staff_user()
        self.client = APIClient()
        self.client.force_authenticate(user=admin)

    def authenticate_simple_user_client(self):
        simple_user = create_simple_user()
        self.client = APIClient()
        self.client.force_authenticate(user=simple_user)

    def create_currency_pair_list(self):
        create_eur_gbp_pair()
        create_eur_jpy_pair()
        create_gbp_jpy_pair()


class TestCurrencyPairListEndpoint(SetUpMixin):
    """ Tests with admin authentication """

    def setUp(self) -> None:
        self.authenticate_admin_client()
        self.url = reverse("currency-pair-list")

    def test_create_currency_pair(self):
        data = {
            **eur_gbp_data,
            "base_currency": create_eur_currency().pk,
            "quote_currency": create_gbp_currency().pk,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = CurrencyPairSerializer(
            CurrencyPair.objects.get(pk=response.data["id"])
        )
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_currency_pair_list(self):
        self.create_currency_pair_list()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CurrencyPairSerializer(
            CurrencyPair.objects.all(), many=True
        )
        self.assertEqual(response.data, serializer.data)


class TestCurrencyPairListEndpointForNonAdmin(SetUpMixin):
    """ Test the permission non-admin users have over the enndpoint. """

    def setUp(self) -> None:
        self.authenticate_simple_user_client()
        self.url = reverse("currency-pair-list")

    def test_create_currency_pair(self):
        """ Non-admin users cannot create currency pairs. """
        data = {
            **eur_gbp_data,
            "base_currency": create_eur_currency().pk,
            "quote_currency": create_gbp_currency().pk,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_currency_pair_list(self):
        """ Authenticated users can retrieve the list of currency pairs. """
        self.create_currency_pair_list()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CurrencyPairSerializer(
            CurrencyPair.objects.all(), many=True
        )
        self.assertEqual(response.data, serializer.data)
