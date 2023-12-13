from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from countries.models import EconomicReport
from countries.api.serializers import EconomicReportSerializer

from tests.utils.accounts import get_or_create_test_user

from tests.utils.reports import (
    get_or_create_us_economic_report,
    get_or_create_economic_report_list,
)

from tests.utils.indicators import get_or_create_us_economic_indicator


class TestEconomicReportList(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = get_or_create_test_user()
        self.client.force_authenticate(user)
        self.url = reverse("economic-report-list")

    def test_economic_report_list(self):
        reports = get_or_create_economic_report_list()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = EconomicReportSerializer(
            EconomicReport.objects.all(),
            many=True,
        )
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(EconomicReport.objects.count() > 0)
        self.assertEqual(EconomicReport.objects.count(), len(reports))

    def test_create_economic_Report(self):
        indicator = get_or_create_us_economic_indicator()
        response = self.client.post(
            self.url,
            data={
                "name": "Relased of Unemployment Rate (YoY)",
                "description": "...",
                "impact_level": 3,
                "datetime": "2023-12-12T12:00:00.00Z",
                "economic_indicator": indicator.pk,
                "unit": "%",
                "actual": 5.5,
                "forecast": 4.5,
                "previous": 5.5,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = EconomicReportSerializer(
            EconomicReport.objects.get(pk=response.data["id"])
        )
        self.assertEqual(response.data, serializer.data)


class TestEconomicReportDetail(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = get_or_create_test_user()
        self.client.force_authenticate(user)
        self.report = get_or_create_us_economic_report()
        self.url = reverse(
            "economic-report-detail",
            kwargs={"pk": self.report.pk},
        )

    def test_retrieve_report(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = EconomicReportSerializer(
            EconomicReport.objects.get(pk=self.report.pk)
        )
        self.assertEqual(response.data, serializer.data)

    def test_update_report(self):
        response = self.client.patch(
            self.url,
            data={
                "name": "ADP Employment Change(YoY)",
                "description": "New Description",
                "impact_level": 2,
                "datetime": "2023-12-14T13:00:00.00Z",
                "actual": 105000,
                "forecast": 130000,
                "previous": 106000,
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = EconomicReportSerializer(
            EconomicReport.objects.get(pk=self.report.pk)
        )
        self.assertEqual(response.data, serializer.data)
