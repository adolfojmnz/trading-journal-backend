from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from countries.models import Country
from countries.api.serializers import CountrySerializer

from tests.utils.accounts import get_or_create_test_admin

from tests.utils.assets import get_or_create_eur_currency

from tests.utils.countries import (
    get_or_create_ge_country,
    get_or_create_country_list,
)


class TestCountryList(TestCase):
    def setUp(self):
        user = get_or_create_test_admin()
        self.client = APIClient()
        self.client.force_authenticate(user)
        self.url = reverse("country-list")
        return super().setUp()

    def test_create_country(self):
        response = self.client.post(
            self.url,
            data={
                "name": "Germany",
                "code": "GE",
                "currency": get_or_create_eur_currency().pk,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = CountrySerializer(
            Country.objects.get(pk=response.data["id"])
        )
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_country_list(self):
        db_countries = get_or_create_country_list()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CountrySerializer(Country.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(Country.objects.count() > 0)
        self.assertEqual(Country.objects.count(), len(db_countries))


class TestCountryDetail(TestCase):
    def setUp(self):
        self.db_country = get_or_create_ge_country()
        user = get_or_create_test_admin()
        self.client = APIClient()
        self.client.force_authenticate(user)
        self.url = reverse(
            "country-detail",
            kwargs={"pk": self.db_country.pk},
        )
        return super().setUp()

    def test_retrieve_country(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CountrySerializer(self.db_country)
        self.assertEqual(response.data, serializer.data)

    def test_update_country(self):
        response = self.client.patch(
            self.url,
            data={"name": "Federal Republic of Germany"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CountrySerializer(
            Country.objects.get(pk=self.db_country.pk)
        )
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data["name"], "Federal Republic of Germany")
