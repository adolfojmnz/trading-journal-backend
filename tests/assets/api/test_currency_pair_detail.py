from json import dumps

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from assets.models import CurrencyPair
from assets.api.serializers import CurrencyPairSerializer

from tests.helpers.assets.forex.pair import create_eur_gbp_pair
from tests.helpers.users import create_staff_user, create_simple_user


class SetUpMixin(TestCase):

    def setUp(self) -> None:
        self.currency_pair = create_eur_gbp_pair()
        self.url = reverse(
            "currency-pair-detail",
            kwargs={"pk": self.currency_pair.pk},
        )

    def authenticate_admin_client(self):
        admin = create_staff_user()
        self.client = APIClient()
        self.client.force_authenticate(user=admin)

    def authenticate_simple_user_client(self):
        simple_user = create_simple_user()
        self.client = APIClient()
        self.client.force_authenticate(user=simple_user)

    def get_serialized_object(self):
        return CurrencyPairSerializer(
            CurrencyPair.objects.get(pk=self.currency_pair.pk)
        )


class TestCurrencyPairDetailEndpoint(SetUpMixin):
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
        data = {"swap_long": -7, "swap_short": 2.98}
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


class TestCurrencyPairDetailEndpointForNonAdmin(SetUpMixin):
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
        data = {"pnl_multiplier": 1000}
        response = self.client.post(self.url,
                                    data=dumps(data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_currency_pair(self):
        """ Non-admin users cannot delete currency pairs. """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)