from json import dumps

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from assets.models import CurrencyPair
from assets.serializers import CurrencyPairSerializer

from accounts.utils import create_test_admin, create_test_user
from assets.helpers.test_utils import (
    create_eur,
    create_gbp,
    create_eurgbp_pair,
    create_currency_pair_list,
)


class SetUpMixin(TestCase):

    def authenticate_admin_client(self):
        admin = create_test_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=admin)

    def authenticate_simple_user_client(self):
        simple_user = create_test_user()
        self.client = APIClient()
        self.client.force_authenticate(user=simple_user)


class TestCurrencyPairList(SetUpMixin):
    """ Tests with admin authentication """

    def setUp(self) -> None:
        self.authenticate_admin_client()
        self.url = reverse("currency-pair-list")

    def test_create_currency_pair(self):
        data = {
            "name": "EUR/GBP Forex Pair",
            "base_currency": create_eur().pk,
            "quote_currency": create_gbp().pk,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = CurrencyPairSerializer(
            CurrencyPair.objects.get(pk=response.data["id"])
        )
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_currency_pair_list(self):
        create_currency_pair_list()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CurrencyPairSerializer(
            CurrencyPair.objects.all(), many=True
        )
        self.assertEqual(response.data, serializer.data)


class TestCurrencyPairListForNonAdmin(SetUpMixin):
    """ Test the permission non-admin users have over the enndpoint. """

    def setUp(self) -> None:
        self.authenticate_simple_user_client()
        self.url = reverse("currency-pair-list")

    def test_create_currency_pair(self):
        """ Non-admin users cannot create currency pairs. """
        data = {
            "name": "EUR/GBP Forex Pair",
            "base_currency": create_eur().pk,
            "quote_currency": create_gbp().pk,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_currency_pair_list(self):
        """ Authenticated users can retrieve the list of currency pairs. """
        create_currency_pair_list()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CurrencyPairSerializer(
            CurrencyPair.objects.all(), many=True
        )
        self.assertEqual(response.data, serializer.data)


class SetUpMixin(TestCase):

    def setUp(self) -> None:
        self.currency_pair = create_eurgbp_pair()
        self.url = reverse(
            "currency-pair-detail",
            kwargs={"pk": self.currency_pair.pk},
        )

    def authenticate_admin_client(self):
        admin = create_test_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=admin)

    def authenticate_simple_user_client(self):
        simple_user = create_test_user()
        self.client = APIClient()
        self.client.force_authenticate(user=simple_user)

    def get_serialized_object(self):
        return CurrencyPairSerializer(
            CurrencyPair.objects.get(pk=self.currency_pair.pk)
        )


class TestCurrencyPairDetail(SetUpMixin):
    """ Tests the endpoint with admin authentication """

    def setUp(self) -> None:
        self.authenticate_admin_client()
        return super().setUp()

    def test_retrieve_currency_pair(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = self.get_serialized_object()
        self.assertEqual(response.data, serializer.data)

    def test_update_currency_pair(self):
        data = {"name": "New name", "pip_decimal_points": 2}
        response = self.client.patch(self.url,
                                     data=dumps(data),
                                     content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = self.get_serialized_object()
        self.assertEqual(response.data, serializer.data)

    def test_delete_currency_pair(self):
        """ This tests passes because the currency pair to be
            deleted in not associate to other instances. """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestCurrencyPairDetailForNonAdmin(SetUpMixin):
    """ Test the endpoint with non-admin authentication. """

    def setUp(self) -> None:
        self.authenticate_simple_user_client()
        return super().setUp()

    def test_retrieve_currency_pair(self):
        """ Authenticated users can retrieve currency pairs. """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = self.get_serialized_object()
        self.assertEqual(response.data, serializer.data)

    def test_update_currency_pair(self):
        data = {"pip_decimal_position": 2}
        response = self.client.post(self.url,
                                    data=dumps(data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_currency_pair(self):
        """ Non-admin users cannot delete currency pairs. """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)