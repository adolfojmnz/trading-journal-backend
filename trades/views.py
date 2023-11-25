from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from trades.serializers import (
    TradeSerializer,
    MetricsSummarySerializer,
    ProfitAndLossSerializer,
    TotalTradesSerializer,
    HoldingTimeSerializer,
    PositionVolumeSerializer,
)
from trades.view_mixins import TradeViewMixin, MetricsViewMixin


class TradeListView(TradeViewMixin, ListCreateAPIView):
    serializer_class = TradeSerializer


class TradeDetailView(TradeViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = TradeSerializer


class MetricsSummaryView(MetricsViewMixin):
    serializer_class = MetricsSummarySerializer


class ProfitAndLossView(MetricsViewMixin):
    serializer_class = ProfitAndLossSerializer


class TotalTradesView(MetricsViewMixin):
    serializer_class = TotalTradesSerializer


class HoldingTimeView(MetricsViewMixin):
    serializer_class = HoldingTimeSerializer


class PositionVolumeView(MetricsViewMixin):
    serializer_class = PositionVolumeSerializer
