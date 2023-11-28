from django.urls import path

from metrics.api.views.trades import (
    MetricsSummaryView,
    ProfitAndLossView,
    TotalTradesView,
    HoldingTimeView,
    PositionVolumeView,
)


urlpatterns = [
    path(
        "trades/metrics",
        MetricsSummaryView.as_view(),
        name="metrics-summary",
    ),
    path(
        "trades/metrics/pnl",
        ProfitAndLossView.as_view(),
        name="metrics-pnl",
    ),
    path(
        "trades/metrics/total",
        TotalTradesView.as_view(),
        name="metrics-totals",
    ),
    path(
        "trades/metrics/holding-time",
        HoldingTimeView.as_view(),
        name="metrics-holding-time",
    ),
    path(
        "trades/metrics/volume",
        PositionVolumeView.as_view(),
        name="metrics-volume",
    ),
]
