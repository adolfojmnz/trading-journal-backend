from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from trades.models import Trade
from trades.filters import TradeFilterBackend, TradeFilterSet

from metrics.api.serializers.trades import (
    MetricsSummarySerializer,
    ProfitAndLossSerializer,
    TotalTradesSerializer,
    HoldingTimeSerializer,
    PositionVolumeSerializer,
)


class MetricsViewMixin(GenericAPIView):
    model = Trade
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [TradeFilterBackend]
    filterset_class = TradeFilterSet

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            user=self.request.user
        )
        return self.filter_queryset(queryset)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            self.get_queryset(),
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
