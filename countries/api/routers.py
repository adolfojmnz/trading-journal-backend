from django.urls import path

from countries.api.views import (
    CountryListView,
    CountryDetailView,
    EconomicReportListView,
    EconomicReportDetailView,
    EconomicIndicatorListView,
    EconomicIndicatorDetailView,
)


urlpatterns = [
    path(
        "countries",
        CountryListView.as_view(),
        name="country-list",
    ),
    path(
        "countries/<int:pk>",
        CountryDetailView.as_view(),
        name="country-detail",
    ),
    path(
        "reports",
        EconomicReportListView.as_view(),
        name="economic-report-list",
    ),
    path(
        "reports/<int:pk>",
        EconomicReportDetailView.as_view(),
        name="economic-report-detail",
    ),
    path(
        "indicators",
        EconomicIndicatorListView.as_view(),
        name="economic-indicator-list",
    ),
    path(
        "indicators/<int:pk>",
        EconomicIndicatorDetailView.as_view(),
        name="economic-indicator-detail",
    ),
]
