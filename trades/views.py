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

from trades.serializers import TradeMetricsSerializer


class TradeQuerysetMixin:
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class TradeMetricsView(APIView):
    serializer_class = TradeMetricsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request, data=request.data)
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