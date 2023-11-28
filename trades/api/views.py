from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from trades.models import Trade
from trades.api.serializers import TradeSerializer
from trades.api.filters import TradeFilterBackend, TradeFilterSet


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


class TradeListView(TradeViewMixin, ListCreateAPIView):
    serializer_class = TradeSerializer


class TradeDetailView(TradeViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = TradeSerializer
