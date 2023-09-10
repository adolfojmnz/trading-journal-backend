from django.urls import path

from assets.api import views


urlpatterns = [
    # Currency
    path("currencies", views.CurrencyListView.as_view(), name="currency-list"),
    path("currencies/<int:pk>", views.CurrencyDetailView.as_view(), name="currency-detail"),

    # Currency Pair
    path("currency-pairs", views.CurrencyPairListView.as_view(), name="currency-pair-list"),
    path("currency-pairs/<int:pk>", views.CurrencyPairDetailView.as_view(), name="currency-pair-detail"),
]