from rest_framework.views import APIView
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


class MetricsSummaryView(MetricsViewMixin, APIView):
    serializer_class = MetricsSummarySerializer


class ProfitAndLossView(MetricsViewMixin, APIView):
    serializer_class = ProfitAndLossSerializer


class TotalTradesView(MetricsViewMixin, APIView):
    serializer_class = TotalTradesSerializer


class HoldingTimeView(MetricsViewMixin, APIView):
    serializer_class = HoldingTimeSerializer


class PositionVolumeView(MetricsViewMixin, APIView):
    serializer_class = PositionVolumeSerializer
