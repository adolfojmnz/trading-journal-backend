from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from operations.models import ForexOperation
from operations.api.serializers import ForexOperationSerializer


class GetQuerysetMixin:
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(
            trading_account__user=self.request.user
        )


class ForexOperationListView(GetQuerysetMixin, ListCreateAPIView):
    model = ForexOperation
    queryset = model.objects.all()
    serializer_class = ForexOperationSerializer


class ForexOperationDetailView(GetQuerysetMixin, RetrieveUpdateDestroyAPIView):
    model = ForexOperation
    queryset = model.objects.all()
    serializer_class = ForexOperationSerializer
