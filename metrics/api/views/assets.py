from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from assets.models import CurrencyPair

from metrics.api.serializers.assets import AssetMetricsSerializer


class AssetMetricsView(GenericAPIView):
    model = CurrencyPair
    queryset = model.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AssetMetricsSerializer

    def get_object(self):
        return super().get_object()

    def get(self, request, *args, **kwargs):
        asset = self.get_object()
        queryset = asset.trade_set.filter(user=request.user)
        serializer = self.serializer_class(
            queryset,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
