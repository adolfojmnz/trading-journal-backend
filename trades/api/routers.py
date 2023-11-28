from django.urls import path

from trades.api.views import TradeListView, TradeDetailView


urlpatterns = [
    path(
        "trades",
        TradeListView.as_view(),
        name="trade-list",
    ),
    path(
        "trades/<int:pk>",
        TradeDetailView.as_view(),
        name="trade-detail",
    ),
]
