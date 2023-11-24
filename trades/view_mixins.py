from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from trades.models import Trade
from trades.filters import TradeFilterBackend, TradeFilterSet


class TradeViewMixin:
    model = Trade
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [TradeFilterBackend]
    filterset_class = TradeFilterSet

    def get_queryset(self):
        return super().get_queryset().filter(
            user=self.request.user
        )


class MetricsViewMixin:
    model = Trade
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [TradeFilterBackend]
    filterset_class = TradeFilterSet

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user
        )

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            self.get_queryset(),
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
