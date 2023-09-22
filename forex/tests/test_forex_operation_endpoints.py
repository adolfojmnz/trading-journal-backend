from json import dumps

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from accounts.utils import create_test_user, create_test_admin

from forex.models import ForexOperation
from forex.serializers import ForexOperationSerializer
from forex.utils import (
    create_eurgbp_pair,
    create_forex_operation,
    create_forex_operation_list,
)


class TestForexOperationListEndpoint(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_test_user()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("forex-operation-list")
        return super().setUp()

    def test_create_operation(self):
        response = self.client.post(
            self.url,
            data={
                "user": self.user.pk,
                "type": "L",
                "currency_pair": create_eurgbp_pair().pk,
                "opened_on": timezone.now(),
                "closed_on": timezone.now(),
                "open_price": 1.25467,
                "close_price": 1.25667,
                "pnl": 20,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = ForexOperationSerializer(
            ForexOperation.objects.get(pk=response.data["id"])
        )
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_operation_list(self):
        create_forex_operation_list(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ForexOperationSerializer(
            ForexOperation.objects.all(), many=True
        )
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(ForexOperation.objects.count() > 0)


class TestForexOperationDetail(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_test_user()
        self.client.force_authenticate(user=self.user)
        self.operation = create_forex_operation(self.user)
        self.url = reverse("forex-operation-detail",
                           kwargs={"pk": self.operation.pk})
        return super().setUp()

    def test_retrive_forex_operation(self):
        response = self.client.get(self.url)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        serializer = ForexOperationSerializer(
            ForexOperation.objects.get(pk=response.data["id"])
        )
        self.assertEqual(response.data, serializer.data)

    def test_update_forex_operation(self):
        data = {"type": "S", "pnl": -60}
        response = self.client.patch(self.url,
                                     data=dumps(data),
                                     content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ForexOperationSerializer(
            ForexOperation.objects.get(pk=response.data["id"])
        )
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(serializer.instance.pnl, -60)
        self.assertEqual(serializer.instance.type, "S")

    def test_delete_forex_operation(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestForexOperationQuerySet(TestCase):
    """ Test that forex operations are only retrievable by their owners """

    def setUp(self) -> None:
        self.client = APIClient()
        user = create_test_user()
        admin = create_test_admin()
        self.client.force_authenticate(user=admin)
        self.operation = create_forex_operation(user)
        self.url = reverse("forex-operation-detail",
                           kwargs={"pk": self.operation.pk})
        return super().setUp()

    def test_retrieve_forex_operation(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_forex_operation(self):
        data = {"type": "S", "pnl": -60}
        response = self.client.patch(self.url,
                                     data=dumps(data),
                                     content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_forex_operation(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)