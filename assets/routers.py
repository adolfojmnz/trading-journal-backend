from django.urls import path

from assets import views


urlpatterns = [
    path(
        "currencies",
        views.CurrencyListView.as_view(),
        name="currency-list",
    ),
    path(
        "currencies/<int:pk>",
        views.CurrencyDetailView.as_view(),
        name="currency-detail",
    ),
    path(
        "assets/",
        views.CurrencyPairListView.as_view(),
        name="pair-list",
    ),
    path(
        "assets/<int:pk>",
        views.CurrencyPairDetailView.as_view(),
        name="pair-detail",
    ),
]
