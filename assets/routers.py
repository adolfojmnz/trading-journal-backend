from django.urls import path

from assets import views


urlpatterns = [
    # Currency
    path("assets/currencies", views.CurrencyListView.as_view(), name="currency-list"),
    path("assets/currencies/<int:pk>", views.CurrencyDetailView.as_view(), name="currency-detail"),

    # Currency Pair
    path("assets/currency-pairs", views.CurrencyPairListView.as_view(), name="currency-pair-list"),
    path("assets/currency-pairs/<int:pk>", views.CurrencyPairDetailView.as_view(), name="currency-pair-detail"),
]