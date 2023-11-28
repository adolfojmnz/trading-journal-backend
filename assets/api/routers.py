from django.urls import path

from assets.api.views import (
    CurrencyListView,
    CurrencyDetailView,
    CurrencyPairListView,
    CurrencyPairDetailView,
)


urlpatterns = [
    path(
        "currencies",
        CurrencyListView.as_view(),
        name="currency-list",
    ),
    path(
        "currencies/<int:pk>",
        CurrencyDetailView.as_view(),
        name="currency-detail",
    ),
    path(
        "assets/",
        CurrencyPairListView.as_view(),
        name="pair-list",
    ),
    path(
        "assets/<int:pk>",
        CurrencyPairDetailView.as_view(),
        name="pair-detail",
    ),
]
