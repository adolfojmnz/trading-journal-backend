from django.urls import path

from trades.views import TradeListView, TradeDetailView, TradeMetricsView


urlpatterns = [
    path("trades", TradeListView.as_view(), name="trade-list"),
    path("trades/<int:pk>", TradeDetailView.as_view(), name="trade-detail"),
    path("trades/metrics", TradeMetricsView.as_view(), name="trades-metrics"),
]