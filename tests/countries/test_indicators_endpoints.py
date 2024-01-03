from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from countries.models import (
    EconomicIndicator,
)

from countries.api.serializers import (
    EconomicIndicatorSerializer,
)

from tests.utils.accounts import get_or_create_test_admin

from tests.utils.countries import get_or_create_ch_country

from tests.utils.indicators import (
    get_or_create_us_economic_indicator,
    get_or_create_economic_indicator_list,
)


class TestEconomicIndicatorList(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = get_or_create_test_admin()
        self.client.force_authenticate(user)
        self.url = reverse("economic-indicator-list")

    def test_indicator_list(self):
        indicators = get_or_create_economic_indicator_list()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = EconomicIndicatorSerializer(
            EconomicIndicator.objects.all(),
            many=True,
        )
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(EconomicIndicator.objects.count() > 0)
        self.assertEqual(EconomicIndicator.objects.count(), len(indicators))

    def test_create_economic_indicator(self):
        response = self.client.post(
            self.url,
            data={
                "country": get_or_create_ch_country().pk,
                "name": "Unemployment Rate (YoY)",
                "description": "...",
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = EconomicIndicatorSerializer(
            EconomicIndicator.objects.get(pk=response.data["id"])
        )
        self.assertEqual(response.data, serializer.data)


class TestEconomicIndicatorDetail(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = get_or_create_test_admin()
        self.client.force_authenticate(user)
        self.indicator = get_or_create_us_economic_indicator()
        self.url = reverse(
            "economic-indicator-detail",
            kwargs={"pk": self.indicator.pk},
        )

    def test_retrieve_indicator(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = EconomicIndicatorSerializer(self.indicator)
        self.assertEqual(response.data, serializer.data)

    def test_update_indicator(self):
        response = self.client.patch(
            self.url,
            data={"name": "ADP Employment Change (YoY)"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = EconomicIndicatorSerializer(
            EconomicIndicator.objects.get(pk=self.indicator.pk)
        )
        self.assertEqual(response.data, serializer.data)
