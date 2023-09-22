from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAdminUser,
    IsAuthenticated,
)

from forex.models import Currency, CurrencyPair, ForexOperation
from forex.serializers import (
    CurrencySerializer,
    CurrencyPairSerializer,
    ForexOperationSerializer,
)


class GetPermissionsMixin:
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if not self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class CurrencyListView(GetPermissionsMixin, ListCreateAPIView):
    model = Currency
    queryset = model.objects.all()
    serializer_class = CurrencySerializer


class CurrencyDetailView(GetPermissionsMixin, RetrieveUpdateDestroyAPIView):
    model = Currency
    queryset = model.objects.all()
    serializer_class = CurrencySerializer


class CurrencyPairListView(GetPermissionsMixin, ListCreateAPIView):
    model = CurrencyPair
    queryset = model.objects.all()
    serializer_class = CurrencyPairSerializer


class CurrencyPairDetailView(GetPermissionsMixin, RetrieveUpdateDestroyAPIView):
    model = CurrencyPair
    queryset = model.objects.all()
    serializer_class = CurrencyPairSerializer


class GetQuerysetMixin:
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ForexOperationListView(GetQuerysetMixin, ListCreateAPIView):
    model = ForexOperation
    queryset = model.objects.all()
    serializer_class = ForexOperationSerializer


class ForexOperationDetailView(GetQuerysetMixin, RetrieveUpdateDestroyAPIView):
    model = ForexOperation
    queryset = model.objects.all()
    serializer_class = ForexOperationSerializer