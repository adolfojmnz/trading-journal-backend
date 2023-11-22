from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from trades.models import Trade
from trades.serializers import TradeSerializer

from trades.serializers import (
    MetricsSummarySerializer,
    ProfitAndLossSerializer,
    TotalTradesSerializer,
    HoldingTimeSerializer,
    PositionVolumeSerializer,
)


class TradeQuerysetMixin:
    permission_classes = []

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class MetricsMixin(APIView):
    model = Trade
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(
                open_datetime__date=date
            )
        return queryset

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            self.get_queryset(),
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TradeListView(TradeQuerysetMixin, ListCreateAPIView):
    model = Trade
    queryset = model.objects.all()
    serializer_class = TradeSerializer


class TradeDetailView(TradeQuerysetMixin, RetrieveUpdateDestroyAPIView):
    model = Trade
    queryset = model.objects.all()
    serializer_class = TradeSerializer


class MetricsSummaryView(MetricsMixin):
    serializer_class = MetricsSummarySerializer


class ProfitAndLossView(MetricsMixin):
    serializer_class = ProfitAndLossSerializer


class TotalTradesView(MetricsMixin):
    serializer_class = TotalTradesSerializer


class HoldingTimeView(MetricsMixin):
    serializer_class = HoldingTimeSerializer


class PositionVolumeView(MetricsMixin):
    serializer_class = PositionVolumeSerializer
